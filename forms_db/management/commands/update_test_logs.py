import os
import paramiko
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from forms_db.models import Uut, TestHistory, Station, Employes, Booms, Failures, ErrorMessages

class Command(BaseCommand):
    help = 'Actualiza logs de prueba desde estaciones remotas'
    
    def handle(self, *args, **options):
        estaciones_dict = {
            "10.12.199.26": "FFT-05",
            # Agrega aquí otras estaciones
        }
        
        for ip, estacion_nombre in estaciones_dict.items():
            try:
                self.process_station(ip, estacion_nombre)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error en estación {estacion_nombre}: {str(e)}'))

    def process_station(self, ip, estacion_nombre):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            client.connect(ip, port=22, username='PMDU', password='Msft02.', timeout=10)
            sftp = client.open_sftp()
            
            try:
                # Verificar/Crear directorio FFT2 log remoto
                try:
                    sftp.stat('C:/Logs Pruebas')
                except FileNotFoundError:
                    sftp.mkdir('C:/Logs Procesados')
                
                archivos_remotos = sftp.listdir('C:/Logs Pruebas')
                
                for archivo in archivos_remotos:
                    if archivo.endswith(("_PASS.txt", "_FAIL.txt")):
                        try:
                            self.process_single_file(sftp, archivo, ip, estacion_nombre)
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f'Error procesando {archivo}: {str(e)}'))
            finally:
                sftp.close()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error de conexión con {ip}: {str(e)}'))
        finally:
            client.close()

    def process_single_file(self, sftp, filename, ip, estacion_nombre):
        remote_path = f"C:/Logs Pruebas/{filename}"
        remote_backup_path = f"C:/Logs Procesados/{filename}"
        is_pass = "_PASS" in filename
        
        try:
            # 1. Primero guardar copia local del archivo original
            log_info = self.save_local_copy(sftp, remote_path, filename, estacion_nombre)
            
            # 2. Luego mover el archivo remoto
            sftp.rename(remote_path, remote_backup_path)
            
            # 3. Solo registrar en BD si es GDL
            if log_info.get('factory', '').upper() == 'GDL':
                if not log_info['sn']:
                    raise ValueError("No se pudo extraer el número de serie del log")
                
                uut = self.register_uut(log_info, is_pass)
                test_history = self.register_test_history(uut, ip, estacion_nombre, log_info, is_pass)
                
                if not is_pass:
                    self.register_failure(uut, ip, estacion_nombre, log_info)
                
                self.stdout.write(self.style.SUCCESS(
                    f"Procesado (GDL): {filename} | SN: {log_info['sn']} | {'PASS' if is_pass else 'FAIL'}"
                ))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f"Procesado (No-GDL): {filename} | SN: {log_info.get('sn', 'N/A')}"
                ))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error procesando archivo {filename}: {str(e)}'
            ))
            raise

    def save_local_copy(self, sftp, remote_path, filename, estacion_nombre):
        """Guarda copia local exacta del archivo original y devuelve la información parseada"""
        try:
            # Obtener ruta base según configuración
            base_dir = Path(settings.STATIC_ROOT)
            
            # Leer y parsear el archivo remoto primero
            with sftp.open(remote_path, 'r') as remote_file:
                # Leer todo el contenido para guardar copia exacta
                file_content = remote_file.read()
                
                # Volver al inicio para parsear
                remote_file.seek(0)
                log_info = self.parse_log_file(remote_file, filename)
            
            # Determinar proyecto (usar 'unknown' si no se puede determinar)
            project = self.determine_project(log_info)
            
            # Crear ruta completa local
            local_dir = base_dir / 'logs' / project / estacion_nombre
            local_path = local_dir / filename
            
            # Asegurar que el directorio existe
            local_dir.mkdir(parents=True, exist_ok=True)
            
            # Guardar copia exacta del archivo original
            with open(local_path, 'wb') as local_file:
                local_file.write(file_content)
            
            self.stdout.write(self.style.SUCCESS(
                f'Copia local guardada en: {local_path}'
            ))
            
            return log_info
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Error guardando copia local {filename}: {str(e)}'
            ))
            raise

    def parse_log_file(self, remote_file, filename):
        """Extrae información del archivo de log"""
        info = {
            'sn': '',
            'operator_id': None,
            'part_number': None,
            'log_datetime': None,
            'error_message': None,
            'station_id': None,
            'factory': None
        }
        
        try:
            # Leer línea por línea para parsear
            for linea in remote_file:
                linea = linea.strip()
                if not info['sn'] and "PPID:" in linea:
                    info['sn'] = linea.split("PPID:")[1].strip()
                elif not info['operator_id'] and "Operator ID:" in linea:
                    info['operator_id'] = linea.split("Operator ID:")[1].strip()
                elif not info['part_number'] and "Part Number:" in linea:
                    info['part_number'] = linea.split("Part Number:")[1].split()[0][:12]
                elif not info['station_id'] and "Station ID:" in linea:
                    info['station_id'] = linea.split("Station ID:")[1].strip()
                elif not info['log_datetime'] and linea.startswith('['):
                    try:
                        datetime_str = linea.split(']')[0][1:]
                        info['log_datetime'] = datetime.strptime(datetime_str, '%Y/%m/%d %H:%M:%S')
                    except ValueError:
                        pass
                elif not info['error_message'] and "_FAIL" in filename and "Failed tests:" in linea:
                    # Leer la siguiente línea para el mensaje de error
                    next_line = next(remote_file, '').strip()
                    if ']' in next_line:
                        info['error_message'] = next_line.split(']', 1)[1].strip()
                    else:
                        info['error_message'] = next_line
                elif "Factory:" in linea:
                    info['factory'] = linea.split("Factory:")[1].strip()
        
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Error leyendo archivo {filename}: {str(e)}'))
        
        # Fallback a información del nombre de archivo
        if not info['sn']:
            info['sn'] = self.extract_serial_from_filename(filename)
        if not info['log_datetime']:
            info['log_datetime'] = self.extract_datetime_from_filename(filename)
        
        return info

    def determine_project(self, log_info):
        """Determina el proyecto basado en el part number"""
        if not log_info.get('part_number'):
            return 'unknown'
        
        try:
            boom = Booms.objects.filter(pn=log_info['part_number']).first()
            return boom.project.lower() if boom else 'unknown'
        except Exception as e:
            self.stdout.write(self.style.WARNING(
                f'Error al determinar proyecto para PN {log_info.get("part_number")}: {str(e)}'
            ))
            return 'unknown'

    def extract_datetime_from_filename(self, filename):
        """Extrae fecha/hora del nombre del archivo"""
        try:
            # Formato esperado: PMDU1.2_P175832760003042_L10_20250418073950_PASS.txt
            parts = filename.split('_')
            if len(parts) >= 4:
                date_str = parts[-2]  # 20250418
                time_str = parts[-1].split('.')[0]  # 073950 de PASS.txt
                return datetime.strptime(f"{date_str}{time_str[:4]}", "%Y%m%d%H%M")
        except (IndexError, ValueError) as e:
            self.stdout.write(self.style.WARNING(
                f'Error extrayendo fecha de {filename}: {str(e)}'
            ))
            return None

    def extract_serial_from_filename(self, filename):
        """Extrae número de serie del nombre del archivo"""
        try:
            # Formato esperado: PMDU1.2_P175832760003042_L10_20250418073950_PASS.txt
            parts = filename.split('_')
            if len(parts) >= 2:
                return parts[1]  # P175832760003042
        except (IndexError, ValueError) as e:
            self.stdout.write(self.style.WARNING(
                f'Error extrayendo SN de {filename}: {str(e)}'
            ))
            return ''

    # ... [Los métodos register_uut, register_test_history, register_failure permanecen iguales] ...

    def register_uut(self, log_info, is_pass):
        """Registra o actualiza una UUT en la base de datos"""
        try:
            employee = None
            if log_info['operator_id']:
                try:
                    employee = Employes.objects.get(employeeNumber=log_info['operator_id'])
                except Employes.DoesNotExist:
                    employee = None
                    self.stdout.write(self.style.WARNING(
                        f'Empleado {log_info["operator_id"]} no encontrado'
                    ))
            
            pn_b = None
            if log_info['part_number']:
                pn_b = Booms.objects.filter(pn=log_info['part_number']).first()
                if not pn_b:
                    self.stdout.write(self.style.WARNING(
                        f'Part Number {log_info["part_number"]} no encontrado en Booms'
                    ))
            
            uut, created = Uut.objects.update_or_create(
                sn=log_info['sn'],
                defaults={
                    'date': log_info['log_datetime'] or timezone.now(),
                    'employee_e': employee,
                    'pn_b': pn_b,
                    'status': not is_pass
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Nueva UUT creada: {log_info["sn"]}'))
            
            return uut
            
        except Exception as e:
            raise ValueError(f'Error registrando UUT: {str(e)}')

    def register_test_history(self, uut, ip, estacion_nombre, log_info, is_pass):
        """Registra el historial de pruebas"""
        try:
            station_name = log_info.get('station_id') or estacion_nombre
            station, _ = Station.objects.get_or_create(stationName=station_name)

            employee = None
            if log_info['operator_id']:
                try:
                    employee = Employes.objects.get(employeeNumber=log_info['operator_id'])
                except Employes.DoesNotExist:
                    employee = None
                    self.stdout.write(self.style.WARNING(
                        f'Empleado {log_info["operator_id"]} no encontrado'
                    ))
            
            return TestHistory.objects.create(
                uut=uut,
                station=station,
                employee_e=employee,
                status=is_pass,
                test_date=log_info['log_datetime'] or timezone.now()
            )
            
        except Exception as e:
            raise ValueError(f'Error registrando TestHistory: {str(e)}')

    def register_failure(self, uut, ip, estacion_nombre, log_info):
        """Registra una falla en la base de datos"""
        try:
            station_name = log_info.get('station_id') or estacion_nombre
            station, _ = Station.objects.get_or_create(stationName=station_name)
            
            employee = None
            if log_info['operator_id']:
                try:
                    employee = Employes.objects.get(employeeNumber=log_info['operator_id'])
                except Employes.DoesNotExist:
                    employee = None
                    self.stdout.write(self.style.WARNING(
                        f'Empleado {log_info["operator_id"]} no encontrado'
                    ))
            
            hour = log_info['log_datetime'].hour if log_info['log_datetime'] else timezone.now().hour
            shift = '1' if 6 <= hour < 14 else '2' if 14 <= hour < 22 else '3'
            
            error_message_obj = None
            if log_info['error_message']:
                try:
                    pn_b = Booms.objects.filter(pn=log_info['part_number']).first() if log_info['part_number'] else None
                    error_message_obj, created = ErrorMessages.objects.get_or_create(
                        message=log_info['error_message'],
                        defaults={
                            'employee_e': employee,
                            'pn_b': pn_b,
                            'date' : timezone.now()
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(
                            f'Nuevo mensaje de error registrado: {log_info["error_message"]}'
                        ))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(
                        f'Error creando ErrorMessage: {str(e)}'
                    ))
            
            failure = Failures.objects.create(
                id_s=station,
                sn_f=uut,
                failureDate=log_info['log_datetime'] or timezone.now(),
                id_er=error_message_obj,
                employee_e=employee,
                shiftFailure=shift,
                analysis='Registro automático - pendiente de análisis',
                rootCause='Por determinar',
                status="False",
                defectSymptom=log_info['error_message'] or 'No especificado',
                correctiveActions='Retest no touch',
                comments=f'Registro automático generado el {timezone.now().strftime("%Y-%m-%d %H:%M")}'
            )
            
            self.stdout.write(self.style.SUCCESS(
                f'Falla registrada para SN: {uut.sn}'
            ))
            
            return failure
            
        except Exception as e:
            raise ValueError(f'Error registrando Falla: {str(e)}')
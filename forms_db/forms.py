from django.forms import ModelForm, PasswordInput, CharField, Textarea, HiddenInput, CharField
from django import forms
from .models import Employes, Uut, Failures, Booms, Rejected, ErrorMessages, Station, Maintenance, SparePart, Release



class EmployeesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'pmd':
                visible.field.widget.attrs['class'] = 'form-check-input'
            elif visible.name == 'dell':
                visible.field.widget.attrs['class'] = 'form-check-input'
            elif visible.name == 'switch':
                visible.field.widget.attrs['class'] = 'form-check-input'
            elif visible.name == 'sony':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
                
    password = CharField(widget=PasswordInput())
    class Meta:
        model = Employes
        fields = '__all__'
    
class UutForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'status':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
            
    class Meta:
        model = Uut
        fields = [
                "sn",
                "pn_b",
                "status"
        ]
        labels = {
                'sn':'Serial Number (SN)',
                'pn_b':'Part Number (PN)',
                'status':'Status'
        }

from django.forms import ModelForm, Textarea, CharField
from .models import Failures

class FailureForm(ModelForm):
    error_message = CharField(
        label="Error Message",
        required=False,
        widget=Textarea(attrs={
            'class': 'form-control mb-2 bg-secondary text-white',
            'readonly': True,
            'disabled': True,
            'rows': 2
        })
    )

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        if instance and instance.id_er:
            initial = kwargs.get('initial', {})
            initial['error_message'] = str(instance.id_er)
            kwargs['initial'] = initial
        
        super().__init__(*args, **kwargs)
        
        # Eliminar campos no editables
        non_editable_fields = ['id_s', 'sn_f', 'shiftFailure', 'log', 'rootCause', 'id_er']
        for field in non_editable_fields:
            self.fields.pop(field, None)
        
        # Configurar campos visibles
        for field_name, field in self.fields.items():
            if field_name == 'status':
                field.widget.attrs['class'] = 'form-check-input activate'
            elif field_name == 'imgEvindence':
                field.widget.attrs['class'] = 'form-control mb-2 text-white bg-black file-input'
            elif field_name != 'error_message':  # Excluir el campo de mensaje de error
                field.widget.attrs['class'] = 'form-control mb-2 text-white bg-black'
    class Meta:
        model = Failures
        fields = ['analysis', 'rootCauseCategory', 'defectSymptom', 
                 'correctiveActions', 'imgEvindence', 'comments']
        labels = {
            'id_er': 'Error Message',
            'analysis': 'Analysis',
            'rootCauseCategory': 'Root Cause Category',
            'defectSymptom': 'Defect Location',
            'correctiveActions': 'Corrective Actions',
            'imgEvindence': 'Image Evidence',
            'comments': 'Comments'
        }

        widgets = {
            'comments': Textarea(attrs={'rows': 3}),
            'correctiveActions': Textarea(attrs={'rows': 2}),
        }
        
class BoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 text-white bg-black'
    class Meta:
        model = Booms
        fields = '__all__'
        exclude = ['employee_e', 'project']
        labels = {'ubiLogic':'Logic ubication',
        'pn':'Part Number (PN)'}

class RejectedForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
    class Meta:
        model = Rejected
        fields = [
            "pn_b",
            "snDamaged",
            "snNew",
            "folio",
        ] 
        labels = {
            'pn_b':'Part Number (PN)',
            'snDamaged':'Serial Number (SN) Damaged',
            'snNew': 'Serial Number (SN) New',
            'folio':'Folio',
        } 
        
class ErrorMessageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
            
    class Meta:
        model = ErrorMessages
        fields = [
            "message",
            "pn_b"
        ]  
        labels = {
            'message':'Error Message',
            'pn_b':'Part Number (PN)'
        }

class StationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
            
    class Meta:
        model = Station
        fields = ['stationProject', 'stationName', 'description']
        labels = {
            'stationProject': 'Project',
            'stationName': 'Name',
            'description': 'Description',
        } 
        

class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = ['id_sp', 'maintenanceType', 'station_s', 'comments']
        labels = {
            'id_sp': 'Spare Part',
            'maintenanceType': 'Maintenance Type',
            'statition_s': 'Station',
            'comments': 'comments',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['id_sp', 'maintenanceType', 'station_s', 'comments']:
            self.fields[field_name].widget.attrs['class'] = 'form-control mb-2 text-white bg-black'
        
        # Utilizar un widget de Select con búsqueda
        self.fields['maintenanceType'].widget = forms.Select(
            choices=Maintenance.maintenance_type_choices,
            attrs={'class': 'form-control mb-2 text-white bg-black'}
        )


    def clean(self):
        cleaned_data = super().clean()
        maintenance_type = cleaned_data.get('maintenanceType')
        date_start = cleaned_data.get('dateStart')
        print(date_start)

        if maintenance_type == 'Preventive':
            cleaned_data['failureM'] = 'N/A'
            cleaned_data['causeCategoryS'] = 'N/A'
        

        return cleaned_data

class CorrectiveMaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = ['id_sp','failureM','causeCategoryS','comments']
        labels = {
            'id_sp': 'Spare Part',
            'failureM': 'Failure Message',
            'causeCategoryS': 'Cause Category',
            'comments': 'Comments',
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['id_sp','comments','failureM','causeCategoryS']:
            self.fields[field_name].widget.attrs['class'] = 'form-control mb-2 text-white bg-black'
        


class SpareForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
            
    class Meta:
        model = SparePart
        fields = ['quantity', 'description', 'pn']
        labels = {
            'quantity': 'Quantity',
            'description': 'Description',
            'pn': 'Part Number (PN)',
        }
        
class ReleaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6 text-white bg-black'
            
    class Meta:
        model = Release
        fields = [
           "serial", "shift", "nicho", "cims", "crabber" 
        ]  
        labels = {
            "serial":'Numero de serie (Sn):', "shift":'Turno:', "cims":'Imagen del Cims:', "crabber":'Imagen de Crabber:', "nicho":'Posicion y Nicho: '
        }

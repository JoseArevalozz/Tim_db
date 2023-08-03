from django.forms import ModelForm, PasswordInput, CharField, Textarea
# from django import forms
from .models import Employes, Uut, Failures, Booms, Rejected, ErrorMessages, Station, Maintenance, SparePart

class EmployeesForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta:
        model = Employes
        fields = '__all__'
    
class UutForm(ModelForm):
    class Meta:
        model = Uut
        fields = [
                "sn",
                "pn_b"
        ]
        labels = {
                'sn':'Serial Number',
                'pn_b':'Part Number (PN)',
        }

class FailureForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'status':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control mb-2 text-white bg-black'
        
    class Meta:
        model = Failures
        fields = ['id_s', 'sn_f', 'id_er', 'analysis', 'rootCause', 'defectSymptom', 'shiftFailure', 'correctiveActions', 'comments'] 
        labels = {'id_s': 'Station', 'sn_f':'SN UUT', 'id_er': 'Error Message', 'analysis': 'Analysis', 'rootCause': 'Root Cause', 'defectSymptom': 'Defect Symptom', 'shiftFailure': 'Shift Failure', 'correctiveActions': 'Corrective Actions', 'comments': 'Comments'}
        widgets = {
          'comments': Textarea(attrs={'rows':1, }),
        }
        
class BoomForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 text-white bg-black'
    class Meta:
        model = Booms
        fields = '__all__'
        labels = {'ubiLogic':'Logic ubication',
        'pn':'Part Number (PN)'}

class RejectedForm(ModelForm):
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
            'snDamaged':'Sn Damaged',
            'snNew': 'Sn New',
            'folio':'Folio',
        } 
        
class ErrorMessageForm(ModelForm):
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
    class Meta:
        model = Station
        fields = ['stationProject', 'stationName', 'description']
        labels = {
            'stationProject': 'Station Project',
            'stationName': 'Station Name',
            'description': 'Descripción',
        } 
        
class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = ['id_sp', 'maintenanceType', 'statition_s', 'employee_e', 'failureM', 'causeCategoryS', 'dateFinish', 'status']
        labels = {
            'id_sp': 'ID Spare Part',
            'maintenanceType': 'Maintenance Type',
            'statition_s': 'Station',
            'employee_e': 'Number Employe',
            'failureM': 'Failure Message',
            'causeCategoryS': 'Cause Category',
            'dateFinish': 'Date Finish',
            'status': 'Status',
        } 

class SpareForm(ModelForm):
    class Meta:
        model = SparePart
        fields = ['quantity', 'description', 'pn']
        labels = {
            'quantity': 'Quantity',
            'description': 'Descripción',
            'pn': 'Part Number (PN)',
        }  
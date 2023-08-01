from django.forms import ModelForm, PasswordInput, CharField
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
        fields = '__all__'

class FailureForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            if visible.name == 'status':
                visible.field.widget.attrs['class'] = 'form-check-input'
            else:
                visible.field.widget.attrs['class'] = 'form-control mb-2 col-md-6 col-sm-6'
        
        print(dir(visible.label_tag))
    class Meta:
        model = Failures
        fields = ['id_s', 'sn_f', 'id_er', 'analysis', 
                  'rootCause', 'status', 'defectSymptom', 'shiftFailure', 
                  'correctiveActions', 'comments'] 
        labels = {'id_s': 'Station', 'sn_f':'SN UUT', 
                  'id_er': 'Error Message', 'analysis': 'Analysis', 'rootCause': 'Root Cause', 'status': 'Status', 'defectSymptom': 'Defect Symptom', 'shiftFailure': 'Shift Failure', 
                  'correctiveActions': 'Corrective Actions', 
                  'comments': 'Comments'}
        
class BoomForm(ModelForm):
    class Meta:
        model = Booms
        fields = '__all__'
        labels = {'ubiLogic':'Logic ubication'}

class RejectedForm(ModelForm):
    class Meta:
        model = Rejected
        fields = '__all__'  
        
class ErrorMessageForm(ModelForm):
    class Meta:
        model = ErrorMessages
        fields = '__all__'  

class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['stationProject', 'stationName', 'description']
        labels = {
            'stationProject': 'Station Project',
            'stationName': 'Station Name',
            'description': 'Description',
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
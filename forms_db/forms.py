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
    class Meta:
        model = Failures
        fields = '__all__'  

class BoomForm(ModelForm):
    class Meta:
        model = Booms
        fields = '__all__'  

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
        fields = '__all__'  
        
class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = '__all__'  

class SpareForm(ModelForm):
    class Meta:
        model = SparePart
        fields = '__all__'  
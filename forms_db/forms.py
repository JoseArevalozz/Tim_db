from django.forms import ModelForm, PasswordInput, CharField
# from django import forms
from .models import Employes, Uut

class EmployeesForm(ModelForm):
    password = CharField(widget=PasswordInput())
    class Meta:
        model = Employes
        fields = '__all__'
    
class UutForm(ModelForm):
    class Meta:
        model = Uut
        fields = '__all__'
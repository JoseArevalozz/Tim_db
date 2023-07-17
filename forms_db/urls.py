from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('employees_form/', views.employeesForm, name='employees_form'),
    path('uut_form/', views.uutForm, name='uut_form')
]
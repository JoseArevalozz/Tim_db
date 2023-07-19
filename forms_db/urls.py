from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('employees_form/', views.employeesForm, name='employees_form'),
    path('uut_form/', views.uutForm, name='uut_form'),
    path('failure_form/', views.failureForm, name='failure_form'),
    path('boom_form/', views.boomForm, name='boom_form'),
    path('rejected_form/', views.rejectedForm, name='rejected_form')
]
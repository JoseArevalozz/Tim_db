from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('employees_form/', views.employeesForm, name='employees_form'),
    path('uut_form/', views.uutForm, name='uut_form'),
    path('failure_form/', views.failureForm, name='failure_form'),
    path('boom_form/', views.boomForm, name='boom_form'),
    path('rejected_form/', views.rejectedForm, name='rejected_form'),
    path('errorMessage_form/', views.errorMessageForm, name='errorMessage_form'),
    path('station_form/', views.stationForm, name='station_form'),
    path('maintenance_form/', views.maintenanceForm, name='maintenance_form'),
    path('spare_form/', views.spareForm, name='spare_form'),
    
    path('user/<str:pk>/', views.userPage, name='user'),
    
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
]
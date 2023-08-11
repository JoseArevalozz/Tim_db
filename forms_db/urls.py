from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('dell/', views.dellView, name='dell'),
    
    path('employees_form/', views.employeesForm, name='employees_form'),
    path('uut_form/', views.uutForm, name='uut_form'),
    path('failure_form/<str:pk>/', views.failureForm, name='failure_form'),
    path('boom_form/', views.boomForm, name='boom_form'),
    path('rejected_form/<str:pk>/', views.rejectedForm, name='rejected_form'),
    path('errorMessage_form/', views.errorMessageForm, name='errorMessage_form'),
    path('station_form', views.stationForm, name='station_form'),
    path('maintenance_form/', views.maintenanceForm, name='maintenance_form'),
    path('spare_form/', views.spareForm, name='spare_form'),
    
    path('showRejecteds/', views.showRejecteds, name='showRejecteds'),
    path('showUuts/', views.showUuts, name='showUuts'),
    
    path('tableRejects/', views.tableRejects, name='tableRejects'),
    
    path('user/<str:pk>/', views.userPage, name='user'),
    
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
]
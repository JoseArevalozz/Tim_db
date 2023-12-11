from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('finish-uut/<str:sn>/', views.finish_uut, name='finish_uut'),
    path('menuRejects/', views.rejectsMenu, name='menuRejects'),
    path('menuMaintenance/', views.maintenanceMenu, name='menuMaintenance'),
    path('menuMetrics/', views.metricMenu, name='menuMetrics'),
    path('employees_form/', views.employeesForm, name='employees_form'),
    path('uut_form/', views.uutForm, name='uut_form'),
    path('failure_form/<str:pk>/', views.failureForm, name='failure_form'),
    path('boom_form/', views.boomForm, name='boom_form'),
    path('rejected_form/<str:pk>/', views.rejectedForm, name='rejected_form'),
    path('errorMessage_form/', views.errorMessageForm, name='errorMessage_form'),
    path('station_form', views.stationForm, name='station_form'),
    path('maintenance_form/', views.maintenanceForm, name='maintenance_form'),
    path('spare_form/', views.spareForm, name='spare_form'),
    path('change_password/', views.passwordForm, name='change_password'),
    path('showRejecteds/', views.showRejecteds, name='showRejecteds'),
    path('showUuts/', views.showUuts, name='showUuts'),
    path('tableRejects/', views.tableRejects, name='tableRejects'),
    path('tableFailures/', views.tableFailures, name='tableFailures'),
    path('tableUuts/', views.tableUuts, name='tableUuts'),
    path('user/<str:pk>/', views.userPage, name='user'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('releaseForm/', views.releaseForm, name='releaseForm'),
    path('table_release/', views.tableRelease, name='table_release')
]
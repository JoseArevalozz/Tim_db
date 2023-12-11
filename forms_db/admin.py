from django.contrib import admin
from .models import Employes, Uut, Failures, Booms, Rejected, ErrorMessages, Station, Maintenance, SparePart, Release
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

class AccountInline(admin.StackedInline):
    model = Employes
    can_delete = False
    verbose_name_plural = 'Employes'   
    
class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)
# ////////////////////////////////////////////////7

class FormEmployees(admin.ModelAdmin):
    list_display = ("employeeNumber", "employeeName", "created")
    search_fields = ("employeeNumber", "employeeName", "created")
    list_filter = ("created", "employeeNumber")
    ordering = ("employeeNumber",)

class FormUuts(admin.ModelAdmin):
    list_display = ("sn", "pn_b", "employee_e")
    search_fields = ("sn", "pn_b", "employee_e")
    list_filter = ("sn", "pn_b", "employee_e")
    ordering = ("sn",)
    
class FormFailures(admin.ModelAdmin):
    list_display = ("sn_f", "status", "failureDate")
    search_fields = ("sn_f", "status", "failureDate")
    list_filter = ("sn_f", "status", "failureDate")
    ordering = ("sn_f",)

class FormBooms(admin.ModelAdmin):
    list_display = ("pn", "description", "project")
    search_fields = ("pn", "description", "project")
    list_filter = ("pn", "description", "project")
    ordering = ("pn",)
    
class FormRejecteds(admin.ModelAdmin):
    list_display = ("id_f", "pn_b", "dateRejected")
    search_fields = ("id_f", "pn_b", "dateRejected")
    list_filter = ("id_f", "pn_b", "dateRejected")
    ordering = ("id_f",)
    
class FormErrors(admin.ModelAdmin):
    list_display = ("message", "date", "employee_e")
    search_fields = ("message", "date", "employee_e")
    list_filter = ("message", "date", "employee_e")
    ordering = ("date",)
    
class FormStations(admin.ModelAdmin):
    list_display = ("stationName", "stationProject", "date")
    search_fields = ("stationName", "stationProject", "date")
    list_filter = ("stationName", "stationProject", "date")
    ordering = ("stationName",)
    
class FormMaintenances(admin.ModelAdmin):
    list_display = ("id_sp", "maintenanceType", "employee_e")
    search_fields = ("id_sp", "maintenanceType", "employee_e")
    list_filter = ("id_sp", "maintenanceType", "employee_e")
    ordering = ("id_sp",)
       
class FormSpares(admin.ModelAdmin):
    list_display = ("pn", "description", "quantity")
    search_fields = ("pn", "description", "quantity")
    list_filter = ("pn", "description", "quantity")
    ordering = ("pn",)
    
class FormRelease(admin.ModelAdmin):
    list_display = ("serial", "employee_e", "nicho")
    search_fields = ("serial", "employee_e", "nicho")
    list_filter = ("serial", "employee_e", "nicho")
    ordering = ("serial",)
    
admin.site.register(Employes, FormEmployees)
admin.site.register(Uut, FormUuts)
admin.site.register(Failures, FormFailures)
admin.site.register(Booms, FormBooms)
admin.site.register(Rejected, FormRejecteds)
admin.site.register(ErrorMessages, FormErrors)
admin.site.register(Station, FormStations)
admin.site.register(Maintenance, FormMaintenances)
admin.site.register(SparePart, FormSpares)
admin.site.register(Release, FormRelease)
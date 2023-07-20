from django.contrib import admin
from .models import Employes, Uut, Failures, Booms, Rejected, ErrorMessages, Station, Maintenance, SparePart

# Register your models here.
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
       
admin.site.register(Employes, FormEmployees)
admin.site.register(Uut, FormUuts)
admin.site.register(Failures, FormFailures)
admin.site.register(Booms, FormBooms)
admin.site.register(Rejected, FormRejecteds)
admin.site.register(ErrorMessages, FormErrors)
admin.site.register(Station)
admin.site.register(Maintenance)
admin.site.register(SparePart)
from django.contrib import admin
from .models import Employes, Uut, Failures, Booms

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
    
admin.site.register(Employes, FormEmployees)
admin.site.register(Uut, FormUuts)
admin.site.register(Failures, FormFailures)
admin.site.register(Booms)
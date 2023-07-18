from django.contrib import admin
from .models import Employes, Uut

# Register your models here.
class FormEmployees(admin.ModelAdmin):
    list_display = ("employee_number", "employee_name", "created")
    search_fields = ("employee_number", "employee_name", "created")
    list_filter = ("created", "employee_number")
    ordering = ("employee_number",)

class FormUuts(admin.ModelAdmin):
    list_display = ("sn", "pn", "employee")
    search_fields = ("sn", "pn", "employee")
    list_filter = ("sn", "pn", "employee")
    ordering = ("sn",)
    
admin.site.register(Employes, FormEmployees)
admin.site.register(Uut, FormUuts)
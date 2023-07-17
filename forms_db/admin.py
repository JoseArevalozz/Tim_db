from django.contrib import admin
from .models import Employes, Uut

# Register your models here.
class FormEmployees(admin.ModelAdmin):
    list_display = ("employee_number", "employee_name", "created")
    search_fields = ("employee_number", "employee_name", "created")
    list_filter = ("created", "employee_number")
    ordering = ("employee_number",)


admin.site.register(Employes, FormEmployees)
admin.site.register(Uut)
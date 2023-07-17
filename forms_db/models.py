from django.db import models

# Create your models here.

class Employes(models.Model):
    employee_number = models.CharField(max_length=10,primary_key=True)
    employee_name = models.CharField(max_length=100)
    password = models.CharField(max_length=30, default='12345')
    pmd = models.BooleanField(default=False)
    dell = models.BooleanField(default=False)
    switch = models.BooleanField(default=False)
    mail = models.CharField(max_length=100, null=True)
    privileges = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now=True)
    
    def __str__(self):
         return self.employee_number

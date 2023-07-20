from django.db import models

# Create your models here.

class Employes(models.Model):
    employeeNumber = models.CharField(max_length=10,primary_key=True)
    employeeName = models.CharField(max_length=100)
    password = models.CharField(max_length=30, default='12345',)
    pmd = models.BooleanField(default=False)
    dell = models.BooleanField(default=False)
    switch = models.BooleanField(default=False)
    mail = models.CharField(max_length=100, null=True)
    privileges = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.employeeName
      
class Booms(models.Model):
    pn = models.CharField(max_length=50, primary_key=True,)
    description = models.CharField(max_length=125)
    commodity = models.CharField(max_length=50)
    product = models.CharField(max_length=30)
    ubiLogic = models.CharField(max_length=15)
    project = models.CharField(max_length=20)
            
    def __str__(self):
        return self.pn

class Uut(models.Model):
    sn = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(auto_now=True)
    pn_b = models.ForeignKey(Booms, on_delete=models.CASCADE)
    employee_e = models.ForeignKey(Employes, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    
    def __str__(self):
         return self.sn

class Station(models.Model):
    idi = models.AutoField(primary_key=True)
    stationProject = models.CharField(max_length=100)
    stationName = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.stationProject

class ErrorMessages(models.Model):
    message = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    employee_e = models.ForeignKey(Employes, on_delete=models.CASCADE)
    pn_b = models.ForeignKey(Booms, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.message
    
class Failures(models.Model):
    id_s = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    sn_f = models.ForeignKey(Uut, on_delete=models.CASCADE, null=True)
    failureDate = models.DateTimeField(auto_now=True)
    id_er = models.ForeignKey(ErrorMessages, on_delete=models.CASCADE, null=True)
    analysis = models.CharField(max_length=100)
    rootCause = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    defectSymptom = models.CharField(max_length=100)
    employee_e  = models.ForeignKey(Employes, on_delete=models.CASCADE)
    shiftFailure = models.CharField(max_length=13)
    correctiveActions = models.CharField(max_length=100)
    comments = models.TextField()
    
    def __str__(self):
        return self.analysis
    
class Rejected(models.Model):
    id_f = models.ForeignKey(Failures, on_delete=models.CASCADE, null=True)
    dateRejected = models.DateTimeField(auto_now=True)
    pn_b = models.ForeignKey(Booms, on_delete=models.CASCADE)
    snDamaged = models.CharField(max_length=50)
    snNew = models.CharField(max_length=50)
    folio = models.CharField(max_length=15)
    employee_e = models.ForeignKey(Employes, on_delete=models.CASCADE)
    
    def __str__(self):
        return ''

class SparePart(models.Model):
    date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    description = models.CharField(max_length=100)
    pn = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description
    
class Maintenance(models.Model):
    id_sp = models.ForeignKey(SparePart, on_delete=models.CASCADE, null=True) 
    maintenanceType = models.CharField(max_length=100)
    station_s = models.ForeignKey(Station, on_delete=models.CASCADE, null=True)
    employee_e = models.ForeignKey(Employes, on_delete=models.CASCADE)
    failureM = models.CharField(max_length=100)
    causeCategoryS = models.CharField(max_length=100)
    dateStart = models.DateTimeField(auto_now=True)
    dateFinish = models.DateTimeField()
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.maintenanceType
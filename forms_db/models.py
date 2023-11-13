from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Employes(models.Model):
    employeeNumber = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # employeeNumber = models.CharField(max_length=10,primary_key=True)
    employeeName = models.CharField(max_length=100)
    pmd = models.BooleanField(default=False)
    dell = models.BooleanField(default=False)
    switch = models.BooleanField(default=False)
    mail = models.CharField(max_length=100, null=True)
    privileges = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.employeeName
      
class Booms(models.Model):
    projects = (('DELL', 'DELL'), ('PMDU', 'PMDU'), ('1G-SW', '1G-SW'))
    
    pn = models.CharField(max_length=50, primary_key=True,)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True,)
    description = models.CharField(max_length=125)
    commodity = models.CharField(max_length=50)
    product = models.CharField(max_length=30, choices=projects)
    ubiLogic = models.CharField(max_length=15,)
    project = models.CharField(max_length=20, choices=projects)
            
    def __str__(self):
        return self.pn
    
        

class Uut(models.Model):
    sn = models.CharField(max_length=50, primary_key=True)
    date = models.DateTimeField(auto_now=True)
    pn_b = models.ForeignKey(Booms,on_delete=models.SET_NULL, blank=True, null=True,)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True,)
    status = models.BooleanField(default=True)
    
    def __str__(self):
         return self.sn

class Station(models.Model):
    projects = (('DELL', 'DELL'), ('PMDU', 'PMDU'), ('1G-SW', '1G-SW'))
    
    stationProject = models.CharField(max_length=50, choices=projects )
    stationName = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.stationName
    
class SparePart(models.Model):
    date = models.DateTimeField(auto_now=True)
    quantity = models.IntegerField()
    description = models.CharField(max_length=100)
    pn = models.CharField(max_length=50)
    
    def __str__(self):
        return self.description
    
class Maintenance(models.Model):
    id_sp = models.ForeignKey(SparePart, on_delete=models.SET_NULL, blank=True, null=True)
    maintenanceType = models.CharField(max_length=100)
    statition_s = models.ForeignKey(Station, on_delete=models.CASCADE)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, default='ex', blank=True, null=True,)
    failureM = models.CharField(max_length=100)
    causeCategoryS = models.CharField(max_length=100)
    dateStart = models.DateTimeField(auto_now=True)
    dateFinish = models.DateTimeField()
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.maintenanceType

class ErrorMessages(models.Model):
    message = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True,)
    pn_b = models.ForeignKey(Booms, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.message    

class Failures(models.Model):
    shifts = (('1', '1'), ('2', '2'), ('3', '3') )
    ca_options = (('Resettled subassy and slaves parts', 'Resettled subassy and slaves parts'), ('Retest in another tester', 'Retest in another tester'), ('Retest no touch', 'Retest no touch'), ('Change component', 'Change component'), ('Clean component', 'Clean component'))
    
    id_s = models.ForeignKey(Station, on_delete=models.SET_NULL, blank=True, null=True,)
    sn_f = models.ForeignKey(Uut, on_delete=models.CASCADE)
    failureDate = models.DateTimeField(auto_now=True)
    id_er = models.ForeignKey(ErrorMessages, on_delete=models.SET_NULL, blank=True, null=True)
    analysis = models.CharField(max_length=100)
    rootCause = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    defectSymptom = models.CharField(max_length=100)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True,)
    shiftFailure = models.CharField(max_length=13, choices=shifts)
    correctiveActions = models.CharField(max_length=100, choices=ca_options)
    imgEvindence = models.ImageField(null=True, upload_to='evidences/', blank=True)
    log = models.FileField(null=True, upload_to='logs/',  blank=True)
    comments = models.TextField()
    
    def __str__(self):
        return self.analysis
    
    
class Rejected(models.Model):
    id_f = models.ForeignKey(Failures, on_delete=models.CASCADE)
    dateRejected = models.DateTimeField(auto_now=True)
    pn_b = models.ForeignKey(Booms, on_delete=models.SET_NULL, blank=True, null=True)
    snDamaged = models.CharField(max_length=50)
    snNew = models.CharField(max_length=50)
    folio = models.CharField(max_length=15)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, default='ex', blank=True, null=True,)
    
    def __str__(self):
        return ''



    
    
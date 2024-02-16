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
    sony = models.BooleanField(default=False)
    mail = models.CharField(max_length=100, null=True)
    privileges = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
         return self.employeeName
      
class Booms(models.Model):
    projects = (('DELL', 'DELL'), ('PMDU', 'PMDU'), ('1G-SW', '1G-SW'), ('SONY', 'SONY'))
    list_products = (('Senna','Senna'), ('Pathfinder','Pathfinder'), ('Sojouner','Sojouner'), ('Hook','Hook'), ('Outlander','Outlander'), ('Minerrall Well','Minerrall Well'), ('MMCs','MCCs'), ('Fornax SAM','Fornax SAM'), ('Fornax DIB','Fornax DIB'), ('Fornax CIT','Fornax CIT'), ('Indus DIB','Indus DIB'), ('Indus BOP','Indus BOP'), ('Indus SAM','Indus SAM'), ('Indus CIT','Indus CIT'), ('PMDU','PMDU'), ('Switch','Switch'), ('Kura', 'Kura'), ('Sled', 'Sled'), ('Rack', 'Rack'))
    
    pn = models.CharField(max_length=50, primary_key=True,)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True,)
    description = models.CharField(max_length=125)
    commodity = models.CharField(max_length=50)
    product = models.CharField(max_length=30, choices=list_products)
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
    projects = (('DELL', 'DELL'), ('PMDU', 'PMDU'), ('1G-SW', '1G-SW'), ('SONY', 'SONY'))
    
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
    maintenance_type_choices = [
        ('Preventive', 'Preventive'),
        ('Corrective', 'Corrective'),
    ]
    maintenanceType = models.CharField(max_length=100, choices=maintenance_type_choices)
    station_s = models.ForeignKey(Station, on_delete=models.CASCADE)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, default='ex', blank=True, null=True)
    dateStart = models.DateTimeField(auto_now_add=True)
    dateFinish = models.DateTimeField()
    status = models.BooleanField(default=True)
    comments = models.CharField(max_length=300, blank=True, null=True)
    failureM = models.CharField(max_length=100, default='N/A')
    causeCategoryS = models.CharField(max_length=100, default='N/A')
    def __str__(self):
        return self.maintenanceType


class ErrorMessages(models.Model):
    message = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now=True)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True,)
    pn_b = models.ForeignKey(Booms, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.message if len(self.message) < 74 else self.message[:73] + '...'

class Failures(models.Model):
    shifts = (('1', '1'), ('2', '2'), ('3', '3') )
    ca_options = (('Resettled subassy and slaves parts', 'Resettled subassy and slaves parts'), ('Retest in another tester', 'Retest in another tester'), ('Retest no touch', 'Retest no touch'), ('Change component', 'Change component'), ('Clean component', 'Clean component'),('reset equipment and retest','reset equipment and retest'))
    
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
    
class Release(models.Model):
    nichos = (('AB19_P01','AB19_P01'),('AB19_P02','AB19_P02'),('AB19_P03','AB19_P03'),('AB19_P04','AB19_P04'),('AB19_P06','AB19_P06'),('AB19_P08','AB19_P08'),('AB19_P09','AB19_P09'),('AB19_P10','AB19_P10'),('AB19_P11','AB19_P11'),('AB19_P12','AB19_P12'),('AB20_P01','AB20_P01'),('AB20_P02','AB20_P02'),('AB20_P03','AB20_P03'),('AB20_P04','AB20_P04'),('AB20_P06','AB20_P06'),('AB20_P08','AB20_P08'),('AB20_P09','AB20_P09'),('AB20_P10','AB20_P10'),('AB20_P11','AB20_P11'),('AB20_P12','AB20_P12'),)
    shifts = (('1','1'),('2','2'), ('3','3'))
    serial = models.CharField(max_length=30, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    nicho = models.CharField(max_length=10, choices=nichos)
    shift = models.CharField(max_length=1, choices=shifts)
    cims = models.ImageField(null=True, upload_to='media/')
    crabber = models.ImageField(null=True, upload_to='media/')
    employee_e = models.ForeignKey(Employes, on_delete = models.SET_NULL, null=True)
    
    def __str__(self):
        return self.serial


class TestHistory(models.Model):
    uut = models.ForeignKey(Uut, on_delete=models.CASCADE)
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    employee_e = models.ForeignKey(Employes, on_delete=models.SET_NULL, blank=True, null=True)
    status = models.BooleanField(default=True)  # True for PASS, False for FAIL
    test_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uut.sn} - {self.station.stationName} - {'PASS' if self.status else 'FAIL'} - {self.test_date}"
    
    
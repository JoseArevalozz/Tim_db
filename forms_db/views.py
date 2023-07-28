from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EmployeesForm, UutForm, FailureForm, BoomForm, RejectedForm, ErrorMessageForm, StationForm, MaintenanceForm, SpareForm
from .models import Uut, Employes, Failures, Station, ErrorMessages
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request=request, template_name='base/first.html',)

def loginUser(request):
    uuts = Uut.objects.all()
    
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('user').lower()
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request=request, message='User does not exist')
            
        user = authenticate(request=request, username=username, password=password)
        
        if user is not None:
            login(request=request, user=user)
            return redirect('home')
        else:
            messages.error(request=request, message='Username or password does not exist')
        
    context={'uuts':uuts}
    return render(request=request, template_name='base/first.html', context=context)


def logoutUser(request):
    logout(request=request)
    return redirect('home')

@login_required(login_url='login')
def employeesForm(request):
    form = EmployeesForm()
    
    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/employee_form.html', context=context)

@login_required(login_url='login')
def uutForm(request):
    form = UutForm()
    
    if request.method == 'POST':
        form = UutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request=request, template_name='base/uut_form.html', context=context)

@login_required(login_url='login')
def failureForm(request):
    form = FailureForm()
   
    if request.method == 'POST':       
    
        station = request.POST.get('id_s')
        uut = request.POST.get('sn_f')
        errorMessage = request.POST.get('id_er')
        user = Employes.objects.get(employeeNumber=request.user)
        
        Failures.objects.create(
            id_s=Station.objects.get(id=(station)),
            sn_f=Uut.objects.get(sn=uut),
            id_er=ErrorMessages.objects.get(id=errorMessage),
            analysis=request.POST.get('analysis'),
            rootCause=request.POST.get('rootCause'),
            status= True if request.POST.get('status') == 'on' else False,
            defectSymptom=request.POST.get('defectSymptom'),
            employee_e=user,
            shiftFailure=request.POST.get('shiftFailure'),
            correctiveActions=request.POST.get('correctiveActions'),
            comments=request.POST.get('comments'),
            
        )
        return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/failure_form.html', context=context)

@login_required(login_url='login')
def boomForm(request):
    form = BoomForm()
    
    if request.method == 'POST':
        form = BoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/boom_form.html', context=context)

@login_required(login_url='login')
def rejectedForm(request):
    form = RejectedForm()
    
    if request.method == 'POST':
        form = RejectedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/rejected_form.html', context=context)

@login_required(login_url='login')
def errorMessageForm(request):
    form = ErrorMessageForm()
    
    if request.method == 'POST':
        form = ErrorMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/errorMessage.html', context=context)

@login_required(login_url='login')
def stationForm(request):
    form = StationForm()
    
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/station_form.html', context=context)

@login_required(login_url='login')
def maintenanceForm(request):
    form = MaintenanceForm()
    
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/maintenance_form.html', context=context)

@login_required(login_url='login')
def spareForm(request):
    form = SpareForm()
    
    if request.method == 'POST':
        form = SpareForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/spare_form.html', context=context)

@login_required(login_url='login')
def userPage(request, pk):
    user = Employes.objects.get(employeeNumber=pk)
    
    context = {'user': user}
    return render(request=request, template_name='base/user.html', context=context)
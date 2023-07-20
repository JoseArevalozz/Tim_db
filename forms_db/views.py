from django.shortcuts import render, redirect
from .forms import EmployeesForm, UutForm, FailureForm, BoomForm, RejectedForm, ErrorMessageForm, StationForm, MaintenanceForm, SpareForm
from .models import Uut

# Create your views here.
def home(request):
    uuts = Uut.objects.all()
    context={'uuts':uuts}
    return render(request=request, template_name='base/first.html', context=context)

def employeesForm(request):
    form = EmployeesForm()
    
    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/employee_form.html', context=context)

def uutForm(request):
    form = UutForm()
    
    if request.method == 'POST':
        form = UutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request=request, template_name='base/uut_form.html', context=context)

def failureForm(request):
    form = FailureForm()
    form.fields['sn_f'].queryset = Uut.objects.filter(status=True)
    if request.method == 'POST':
        form = FailureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/failure_form.html', context=context)

def boomForm(request):
    form = BoomForm()
    
    if request.method == 'POST':
        form = BoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/boom_form.html', context=context)

def rejectedForm(request):
    form = RejectedForm()
    
    if request.method == 'POST':
        form = RejectedForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/rejected_form.html', context=context)

def errorMessageForm(request):
    form = ErrorMessageForm()
    
    if request.method == 'POST':
        form = ErrorMessageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/errorMessage.html', context=context)

def stationForm(request):
    form = StationForm()
    
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/station_form.html', context=context)

def maintenanceForm(request):
    form = MaintenanceForm()
    
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/maintenance_form.html', context=context)

def spareForm(request):
    form = SpareForm()
    
    if request.method == 'POST':
        form = SpareForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form}
    return render(request=request, template_name='base/spare_form.html', context=context)
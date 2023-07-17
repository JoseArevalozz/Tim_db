from django.shortcuts import render, redirect
from .forms import EmployeesForm, UutForm
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
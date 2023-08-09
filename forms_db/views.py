import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EmployeesForm, UutForm, FailureForm, BoomForm, RejectedForm, ErrorMessageForm, StationForm, MaintenanceForm, SpareForm
from .models import Uut, Employes, Failures, Station, ErrorMessages, Booms, Rejected
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


@login_required(login_url='login')
def home(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    context = {'employe': employe}
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')

    return render(request=request, template_name='base/first.html', context=context)

@login_required(login_url='login')
def dellView(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    # if employe.privileges == 'NA':
    #     employe.privileges = 'DELL'
    #     employe.save()
    context = {'employe': employe, 'project': 'dell'}
    
    return render(request=request, template_name='base/first.html', context=context)

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
    employe = Employes.objects.get(employeeNumber=request.user)
    form = EmployeesForm()
    if 'bt-project' in request.POST:
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        form = EmployeesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/employee_form.html', context=context)

@login_required(login_url='login')
def uutForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = UutForm()
    form.fields['pn_b'].queryset = Booms.objects.filter(project=employe.privileges)
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        
        pn_booms = Booms.objects.get(pn=request.POST.get('pn_b'))
        Uut.objects.create(
            sn=request.POST.get('sn'),
            pn_b=pn_booms,
            employee_e=employe,
            status = True if request.POST.get('status') == 'on' else False,
        )
        return redirect('showUuts')
    
    context = {'form':form, 'employe': employe}
    return render(request=request, template_name='base/uut_form.html', context=context)

@login_required(login_url='login')
def failureForm(request, pk):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = FailureForm()
    
    form.fields['id_s'].queryset = Station.objects.filter(stationProject=employe.privileges)
    form.fields['id_er'].queryset = ErrorMessages.objects.filter(pn_b__project=employe.privileges)
    

    uut = Uut.objects.get(sn=pk)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
        return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':  
        if 'bt-project' not in request.POST:
            
            station = request.POST.get('id_s')
            errorMessage = request.POST.get('id_er')
            files = request.FILES  # multivalued dict
            image = files.get("imgEvindence")
            log = files.get('log')
            
            Failures.objects.create(
                id_s=Station.objects.get(id=station),
                sn_f=uut,
                id_er=ErrorMessages.objects.get(id=errorMessage),
                analysis=request.POST.get('analysis'),
                rootCause=request.POST.get('rootCause'),
                status= True if request.POST.get('status') == 'on' else False,
                defectSymptom=request.POST.get('defectSymptom'),
                employee_e=employe,
                imgEvindence=image,
                log=log,
                shiftFailure=request.POST.get('shiftFailure'),
                correctiveActions=request.POST.get('correctiveActions'),
                comments=request.POST.get('comments'),
            )
            return redirect('showRejecteds')
    
    context = {'form': form, 'employe': employe, 'uut': uut}
    return render(request=request, template_name='base/failure_form.html', context=context)

@login_required(login_url='login')
def showUuts(request):
    
    employe = Employes.objects.get(employeeNumber=request.user)
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    uuts = Uut.objects.filter(status=True).filter(pn_b__project=employe.privileges).filter(
        Q(sn__icontains=q) |
        Q(pn_b__pn__icontains=q) |
        Q(date__icontains=q)
    )
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'uuts': uuts, 'employe': employe}
    
    return render(request=request, template_name='base/showUuts.html', context=context)

@login_required(login_url='login')
def boomForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    form = BoomForm()
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        Booms.objects.create(
            pn=request.POST.get('pn'),
            description=request.POST.get('description'),
            commodity=request.POST.get('commodity'),
            product=request.POST.get('product'),
            ubiLogic=request.POST.get('ubiLogic'),
            employee_e=employe,
            project=request.POST.get('project'),
        )
        return redirect('home')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/boom_form.html', context=context)

@login_required(login_url='login')
def rejectedForm(request, pk):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    form = RejectedForm()
    
    form.fields['pn_b'].queryset = Booms.objects.filter(project=employe.privileges)
    # form.fields['sn_f'].queryset = Uut.objects.filter(status=True ).filter(pn_b__project=employe.privileges)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
       
    if request.method == 'POST':
        failure = Failures.objects.get(id=pk)
        pn_booms = Booms.objects.get(pn=request.POST.get('pn_b'))
        
        Rejected.objects.create(
            id_f=failure,
            pn_b=pn_booms,
            snDamaged=request.POST.get('snDamaged'),
            snNew=request.POST.get('snNew'),
            folio=request.POST.get('folio'),
            employee_e=employe
        )
        
        failure.status = False
        failure.save()
        return redirect('showRejecteds')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/rejected_form.html', context=context)

@login_required(login_url='login')
def showRejecteds(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    failures = Failures.objects.filter(status=True).filter(sn_f__pn_b__project=employe.privileges)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'failures': failures, 'employe': employe}
    
    return render(request=request, template_name='base/showRejected.html', context=context)

@login_required(login_url='login')
def errorMessageForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = ErrorMessageForm()
    
    form.fields['pn_b'].queryset = Booms.objects.filter(project=employe.privileges)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        
        pn_booms = Booms.objects.get(pn=request.POST.get('pn_b'))
        
        ErrorMessages.objects.create(
            message=request.POST.get('message'),
            employee_e=employe,
            pn_b=pn_booms
        )
        return redirect('errorMessage_form')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/errorMessage.html', context=context)

@login_required(login_url='login')
def stationForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    form = StationForm()
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/station_form.html', context=context)

@login_required(login_url='login')
def maintenanceForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    form = MaintenanceForm()
    
    form.fields['statition_s'].queryset = Station.objects.filter(stationProject=employe.privileges)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/maintenance_form.html', context=context)

@login_required(login_url='login')
def spareForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = SpareForm()
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        form = SpareForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form': form, 'employe': employe}
    return render(request=request, template_name='base/spare_form.html', context=context)

@login_required(login_url='login')
def userPage(request, pk):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    user = Employes.objects.get(employeeNumber=pk)
    
    context = {'user': user, 'employe':employe}
    return render(request=request, template_name='base/user.html', context=context)

@login_required(login_url='login')
def tableRejects(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    rejects = Rejected.objects.filter(id_f__sn_f__pn_b__project=employe.privileges).filter(
        Q(folio__icontains=q)
    )
    # form = SpareForm()
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('tableRejects')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        check = request.POST.getlist('check')
        response = HttpResponse(content_type="text/csv")

        writer = csv.writer(response)
        writer.writerow(["SN", "Model", "Fail", "PN", 'SN old', 'SN new'])
        
        for checked in check:
            reject = Rejected.objects.get(id=checked)
            
            writer.writerow([reject.id_f.sn_f, reject.id_f.sn_f.pn_b.product, reject.id_f.id_er.message, reject.pn_b.pn, reject.snDamaged, reject.snNew])
            
        response['Content-Disposition'] = 'attachment; filename="expample.csv"'

        return response
        
    
    context = {'employe': employe, 'rejects': rejects}
    return render(request=request, template_name='base/table_rejects.html', context=context)

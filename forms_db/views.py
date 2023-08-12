import csv
import xlwt
from datetime import date, datetime, timedelta
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

def passwordForm(request):
    u = User.objects.get(username__exact=request.user)

    if request.method == 'POST':
        if request.POST.get('new-password') == request.POST.get('val-password'):
            u.set_password(request.POST.get('new-password'))
            u.save()
            return redirect('home')
        else:
            messages.error(request=request, message='The new password its not the same')
    context = {}
    return render(request=request, template_name='base/password_form.html', context=context)

@login_required(login_url='login')
def employeesForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = EmployeesForm()
    if 'bt-project' in request.POST:
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('employees_form')
    
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
            return redirect('uut_form')
    
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
    
    if Uut.objects.filter(sn=pk).exists():
        uut = Uut.objects.get(sn=pk)
        
        if 'bt-project' in request.POST: 
            if request.method == 'POST':
                employe.privileges = request.POST.get('bt-project')
                employe.save()
            return redirect('showUuts')
        
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
    else:
        return redirect('showUuts')
    
    context = {'form': form, 'employe': employe, 'uut': uut}
    return render(request=request, template_name='base/failure_form.html', context=context)

@login_required(login_url='login')
def rejectsMenu(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
        return redirect('menuRejects')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'employe': employe}
    return render(request=request, template_name='base/menuRejects.html', context=context)

@login_required(login_url='login')
def maintenanceMenu(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
        return redirect('menuMaintenance')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context={'employe': employe}
    return render(request=request, template_name='base/menuMaintenance.html', context=context)

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
            return redirect('showUuts')
            
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'uuts': uuts, 'employe': employe, 'search_bt': True}
    
    return render(request=request, template_name='base/showUuts.html', context=context)

@login_required(login_url='login')
def boomForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    form = BoomForm()
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('boom_form')
    
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
            return redirect('showRejecteds')
    
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
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    failures = Failures.objects.filter(status=True).filter(sn_f__pn_b__project=employe.privileges).filter(
        Q(sn_f__sn__icontains=q)
    )
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('showRejecteds')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'failures': failures, 'employe': employe, 'search_bt': True}
    
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
            return redirect('errorMessage_form')
    
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
            return redirect('station_form')
    
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
            return redirect('maintenance_form')
    
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
            return redirect('spare_form')
    
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
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
        return redirect('home')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'user': user, 'employe':employe}
    return render(request=request, template_name='base/user.html', context=context)

@login_required(login_url='login')
def tableRejects(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    try:
        if '/' in q:
            dates = q.split('/')
            
            dateStart = list(map(int, dates[0].split('-')))
            start = date(dateStart[0], dateStart[1], dateStart[2])
            
            dateEnd = list(map(int, dates[1].split('-'))  )     
            end = date(dateEnd[0], dateEnd[1], dateEnd[2])
            new_end = end + timedelta(days=1)
            
            rejects = Rejected.objects.filter(id_f__sn_f__pn_b__project=employe.privileges).filter(
                dateRejected__range=[start, new_end],)
        else:
            rejects = Rejected.objects.filter(id_f__sn_f__pn_b__project=employe.privileges).filter(
                Q(folio__icontains=q)
            )
    except:
        return redirect('tableRejects')
    
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('tableRejects')
    
    if employe.privileges == 'NA':
        return redirect('home')
   
    if request.method == 'POST':
        
        check = request.POST.getlist('check')
        
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        today = datetime.today().strftime("%Y-%m-%d_%H-%M")
        response['Content-Disposition'] = f'attachment; filename="db{today}.xls"'

        #creating workbook
        wb = xlwt.Workbook(encoding='utf-8')

        #adding sheet
        ws = wb.add_sheet("sheet1")

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        # headers are bold
        font_style.font.bold = True

        #column header names, you can use your own headers here
        columns = ["SN", "Model", "Fail", "PN", 'SN old', 'SN new']

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...

        for checked in check:
            reject = Rejected.objects.get(id=checked)
            
            sn = str(reject.id_f.sn_f)
            model = str(reject.id_f.sn_f.pn_b.product)
            message = str(reject.id_f.id_er.message)
            pn = str(reject.pn_b.pn)
            snDamaged = str(reject.snDamaged)
            snNew = str(reject.snNew)
            
            row_num = row_num + 1
            ws.write(row_num, 0, sn, font_style)
            ws.write(row_num, 1, model, font_style)
            ws.write(row_num, 2, message, font_style)
            ws.write(row_num, 3, pn, font_style)
            ws.write(row_num, 4, snDamaged, font_style)
            ws.write(row_num, 5, snNew, font_style)

        wb.save(response)
        return response

    context = {'employe': employe, 'rejects': rejects, 'search_bt': True}
    return render(request=request, template_name='base/table_rejects.html', context=context)




# if request.method == 'POST':
#         check = request.POST.getlist('check')
#         response = HttpResponse(content_type="text/csv")

#         writer = csv.writer(response)
#         writer.writerow(["SN", "Model", "Fail", "PN", 'SN old', 'SN new'])
        
#         for checked in check:
#             reject = Rejected.objects.get(id=checked)
            
#             writer.writerow([reject.id_f.sn_f, reject.id_f.sn_f.pn_b.product, reject.id_f.id_er.message, reject.pn_b.pn, reject.snDamaged, reject.snNew])
        
#         today = datetime.today().strftime("%Y-%m-%d_%H-%M")
#         response['Content-Disposition'] = f'attachment; filename="db{today}.cvs"'

#         return response

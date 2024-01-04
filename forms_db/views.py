import csv
import xlwt
from datetime import date, datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import EmployeesForm, UutForm, FailureForm, BoomForm, RejectedForm, ErrorMessageForm, StationForm, MaintenanceForm, SpareForm, ReleaseForm, CorrectiveMaintenanceForm
from .models import Uut, Employes, Failures, Station, ErrorMessages, Booms, Rejected, Release, Maintenance, SparePart
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone


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
    
    if employe.privileges == 'SONY':
        form.fields['pn_b'].queryset = Booms.objects.filter(Q(commodity='RACK') | Q(commodity='SLED') | Q(commodity='KURA'))
        
    if request.method == 'POST':
        
        pn_booms = Booms.objects.get(pn=request.POST.get('pn_b'))
        try:
            Uut.objects.create(
                sn=request.POST.get('sn'),
                pn_b=pn_booms,
                employee_e=employe,
                status = True if request.POST.get('status') == 'on' else False,
            )
            return redirect('showUuts')
    
        except:
            messages.error(request=request, message='PN already registered!')
    
    context = {'form':form, 'employe': employe}
    return render(request=request, template_name='base/uut_form.html', context=context)

@login_required(login_url='login')
def failureForm(request, pk):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = FailureForm()
    
    if Uut.objects.filter(sn=pk).exists():
        
        
        uut = Uut.objects.get(sn=pk)
        
        if 'Fornax' not in uut.pn_b.product or 'Inuds' not in uut.pn_b.product:
            # pn = str(uut.pn_b)[:5]
            model = uut.pn_b.product
            form.fields['id_er'].queryset = ErrorMessages.objects.filter(pn_b__project=employe.privileges).filter(pn_b__product=model)
            # print(pn)
        else:
            #form.fields['id_er'].queryset = ErrorMessages.objects.filter(pn_b__project=employe.privileges).filter(id_er__pb_b__pn=pn)
            pn = str(uut.pn_b)

        form.fields['id_s'].queryset = Station.objects.filter(stationProject=employe.privileges)
        
        
       
        
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
def metricMenu(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
        return redirect('menuMaintenance')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    context = {'employe':employe}
    return render(request=request, template_name='base/menuMetric.html', context = context)

@login_required(login_url='login')
def showUuts(request):
    
    employe = Employes.objects.get(employeeNumber=request.user)
    
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    
    uuts = Uut.objects.filter(status=True).filter(pn_b__project=employe.privileges).filter(
        Q(sn__icontains=q) |
        Q(pn_b__pn__icontains=q) |
        Q(date__icontains=q)
    ).order_by('-date')

    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('showUuts')
            
    if employe.privileges == 'NA':
        return redirect('home')
    print(uuts)
    context = {'uuts': uuts, 'employe': employe, 'search_bt': True}
    
    return render(request=request, template_name='base/showUuts.html', context=context)

@login_required(login_url='login')
def boomForm(request):
    
    
    employe = Employes.objects.get(employeeNumber=request.user)
    project = employe.privileges
    form = BoomForm()
    # print(form.fields['product'].widget.choices = [(1,1)])
    if project == 'DELL':
        list_products = [('Senna','Senna'), ('Pathfinder','Pathfinder'), ('Sojouner','Sojouner'), ('Hook','Hook'), ('Outlander','Outlander'), ('Minerrall Well','Minerrall Well'), ('MMCs','MCCs'), ('Fornax SAM','Fornax SAM'), ('Fornax DIB','Fornax DIB'), ('Fornax CIT','Fornax CIT'), ('Indus DIB','Indus DIB'), ('Indus BOP','Indus BOP'), ('Indus SAM','Indus SAM'), ('Indus CIT','Indus CIT')]
        
        form.fields['product'].widget.choices = list_products
    if project == 'PMDU':
        list_products = [('PMDU','PMDU')]
        
        form.fields['product'].widget.choices = list_products
    if project == '1G-SW':
        list_products = [('Switch','Switch')]
    if project == 'SONY':
        list_products = [('CRONOS', 'CRONOS')]
        
        form.fields['product'].widget.choices = list_products
        
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('boom_form')
    
    if employe.privileges == 'NA':
        return redirect('home')
    
    if request.method == 'POST':
        # pn_key = Booms.objects.get(pn=request.POST.get('pn'))
        try: 
            Booms.objects.create(
                pn=request.POST.get('pn'),
                description=request.POST.get('description'),
                commodity=request.POST.get('commodity'),
                product=request.POST.get('product'),
                ubiLogic=request.POST.get('ubiLogic'),
                employee_e=employe,
                # project=request.POST.get('project'),
                project=employe.privileges
            )
            
            return redirect('home')
        except:
            messages.error(request=request, message='PN already registered!')
            
        
    
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
    ).order_by('-failureDate')
    
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
    
    if employe.privileges == 'SONY':
        form.fields['pn_b'].queryset = Booms.objects.filter(Q(commodity='RACK') | Q(commodity='SLED') | Q(commodity='KURA'))
    
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

from django.shortcuts import get_object_or_404

@login_required(login_url='login')
def correctiveMaintenanceForm(request, pn_sp, maintenance_id):
    employe = Employes.objects.get(employeeNumber=request.user)

    if employe.privileges == 'NA':
        return redirect('home')

    spare_part = get_object_or_404(SparePart, pn=pn_sp)

    if request.method == 'POST':
        form = CorrectiveMaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = Maintenance.objects.get(id=maintenance_id)

            # Llenar automáticamente employye_e y dateStart
            maintenance.dateFinish = timezone.now()

            # Asignar el SparePart correcto a maintenance.id_sp
            maintenance.id_sp = spare_part

            # Realizar la lógica de reducir la cantidad de SparePart
            if spare_part.quantity > 0:
                spare_part.quantity -= 1 
                spare_part.save()
            else:
                # Si la cantidad es 0, mostrar un mensaje de error o manejar de acuerdo a tus necesidades
                pass
            maintenance.status = False
            maintenance.save()
            return redirect('show_Maintenance')
    else:
        form = CorrectiveMaintenanceForm()

    context = {'form': form, 'pn_sp': pn_sp}
    return render(request, 'base/corrective_maintenance_form.html', context)


@login_required(login_url='login')
def maintenanceForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    
    if employe.privileges == 'NA':
        return redirect('home')

    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            maintenance = form.save(commit=False)
            
            # Llenar automáticamente employye_e y dateStart
            maintenance.employee_e = employe
            maintenance.dateStart = timezone.now()

            # Si el mantenimiento es Corrective, mostrar una nueva vista
            if maintenance.maintenanceType == 'Corrective':

                maintenance.dateFinish = maintenance.dateStart
                maintenance.save()
                
                return redirect('show_Maintenance')


            # Si el mantenimiento es Preventive, establecer dateFinish y salvar
            maintenance.dateFinish = maintenance.dateStart
            maintenance.status = False
            maintenance.save()

            return redirect('home')
    else:
        form = MaintenanceForm()

    form.fields['station_s'].queryset = Station.objects.filter(stationProject=employe.privileges)
    context = {'form': form, 'employe': employe}
    return render(request, 'base/maintenance_form.html', context)

def showMaintenanceForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)

    if employe.privileges == 'NA':
        return redirect('home')

    corrective_instances = Maintenance.objects.filter(
        maintenanceType='Corrective',
        status=True,
        station_s__stationProject=employe.privileges
    ).select_related('station_s', 'id_sp', 'employee_e').order_by('-dateStart')

    context = {'corrective_instances': corrective_instances}
    return render(request, 'base/corrective_stations.html', context)

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
            
            dateEnd = list(map(int, dates[1].split('-')))     
            end = date(dateEnd[0], dateEnd[1], dateEnd[2])
            new_end = end + timedelta(days=1)
            
            rejects = Rejected.objects.filter(id_f__sn_f__pn_b__project=employe.privileges).filter(
                dateRejected__range=[start, new_end],).order_by('-dateRejected')
        else:
            rejects = Rejected.objects.filter(id_f__sn_f__pn_b__project=employe.privileges).filter(
                Q(folio__icontains=q) |
                Q(id_f__sn_f__sn__icontains=q) ).order_by('-dateRejected') 
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
        response['Content-Disposition'] = f'attachment; filename="db{today}.xlsx"'

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
        columns = ['Pn', 'Description', 'Commodity', 'Product', 'Fail Description', 'Sn', 'Sn System', 'Station', 'Folio', 'Qty', 'Ubicacion Logica']

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
            description = str(reject.pn_b.description)
            commodity = str(reject.pn_b.commodity)
            station = str(reject.id_f.id_s.stationName)
            folio = str(reject.folio)
            ubi = str(reject.pn_b.ubiLogic)
            
            row_num = row_num + 1
            ws.write(row_num, 0, pn, font_style)
            ws.write(row_num, 1, description, font_style)
            ws.write(row_num, 2, commodity, font_style)
            ws.write(row_num, 3, model, font_style)
            ws.write(row_num, 4, message, font_style)
            ws.write(row_num, 5, snDamaged, font_style)
            ws.write(row_num, 6, sn, font_style)
            ws.write(row_num, 7, station, font_style)
            ws.write(row_num, 8, folio, font_style)
            ws.write(row_num, 9, str(1), font_style)
            ws.write(row_num, 10, ubi, font_style)

        wb.save(response)
        return response

    context = {'employe': employe, 'rejects': rejects, 'search_bt': True}
    return render(request=request, template_name='base/table_rejects.html', context=context)


def finish_uut(request, sn):
    uut = get_object_or_404(Uut, sn=sn)
    uut.status = False
    uut.save()
    return redirect('showUuts')

@login_required(login_url='login')
def tableFailures(request):
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
            
            failures = Failures.objects.filter(sn_f__pn_b__project=employe.privileges).filter(
                failureDate__range=[start, new_end],)
        else:
            failures = Failures.objects.filter(sn_f__pn_b__project=employe.privileges).filter(
                Q(shiftFailure__icontains=q)
            )
    except:
        return redirect('tableFailures')
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('tableFailures')
    
    if employe.privileges == 'NA':
        return redirect('home')
   
    if request.method == 'POST':
        
        check = request.POST.getlist('check')
        
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        today = datetime.today().strftime("%Y-%m-%d_%H-%M")
        response['Content-Disposition'] = f'attachment; filename="Failures{today}.xls"'

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
        columns = ['Sn', 'Status', 'Failure Date', 'Station', 'Error Message', 'Analysis', 'Root Cause', 'Defect Symptom', 'Employee', 'Failure shift', 'Corrective Actions', 'Comments']

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...

        for checked in check:
            failure = Failures.objects.get(id=checked)
            
            sn = str(failure.sn_f.sn)
            status = str(failure.status)
            date = str(failure.failureDate)
            station = str(failure.id_s.stationName)
            message = str(failure.id_er.message)
            analysis = str(failure.analysis)
            rootCause = str(failure.rootCause)
            defect = str(failure.defectSymptom)
            employee = str(failure.employee_e.employeeName)
            shift = str(failure.shiftFailure)
            correctiveActions = str(failure.correctiveActions)
            comments = str(failure.comments)
            
            row_num = row_num + 1
            ws.write(row_num, 0, sn, font_style)
            ws.write(row_num, 1, status, font_style)
            ws.write(row_num, 2, date, font_style)
            ws.write(row_num, 3, station, font_style)
            ws.write(row_num, 4, message, font_style)
            ws.write(row_num, 5, analysis, font_style)
            ws.write(row_num, 6, rootCause, font_style)
            ws.write(row_num, 7, defect, font_style)
            ws.write(row_num, 8, employee, font_style)
            ws.write(row_num, 9, shift, font_style)
            ws.write(row_num, 10, correctiveActions, font_style)
            ws.write(row_num, 11, comments, font_style)

        wb.save(response)
        return response
    context = {'employe': employe, 'failures': failures}
    return render(request=request, template_name='base/table_fails.html', context=context)

@login_required(login_url='login')
def tableUuts(request):
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
            
            uuts = Uut.objects.filter(pn_b__project=employe.privileges).filter(
                failureDate__range=[start, new_end],)
        else:
            uuts = Uut.objects.filter(pn_b__project=employe.privileges).filter(
                Q(date__icontains=q)
            )
    except:
        return redirect('tableFailures')
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('tableFailures')
    
    if employe.privileges == 'NA':
        return redirect('home')
   
    if request.method == 'POST':
        
        check = request.POST.getlist('check')
        
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')

        #decide file name
        today = datetime.today().strftime("%Y-%m-%d_%H-%M")
        response['Content-Disposition'] = f'attachment; filename="Uuts{today}.xls"'

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
        columns = ['Sn', 'Pn', 'Model', 'Employee', 'Status']

        #write column headers in sheet
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        #get your data, from database or from a text file...

        for checked in check:
            uut = Uut.objects.get(sn=checked)
            
            sn = str(uut.sn)
            pn = str(uut.pn_b.pn)
            model = str(uut.pn_b.product)
            employee = str(uut.employee_e.employeeName)
            status = str(uut.status)
            
            row_num = row_num + 1
            ws.write(row_num, 0, sn, font_style)
            ws.write(row_num, 1, pn, font_style)
            ws.write(row_num, 2, model, font_style)
            ws.write(row_num, 3, employee, font_style)
            ws.write(row_num, 4, status, font_style)

        wb.save(response)
        return response
    context = {'employe': employe, 'uuts': uuts}
    return render(request=request, template_name='base/table_uuts.html', context=context)

@login_required(login_url='login')
def releaseForm(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    form = ReleaseForm()
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('uut_form')
    
    if employe.privileges != 'SONY':
        return redirect('home')
    
    if request.method =='POST':
        files = request.FILES
        cimsI = files.get('cims')
        crabberI = files.get('crabber')
        try:
            Release.objects.create(
                serial = request.POST.get('serial'),
                shift = request.POST.get('shift'),
                nicho = request.POST.get('nicho'),
                cims = cimsI,
                crabber = crabberI,
                employee_e = employe
            )
            return redirect('home')
        except:
            messages.error(request=request, message='SN already registered!')

    context = {'form':form, 'employe':employe}
    return render(request=request, template_name='base/release_form.html', context=context)

@login_required(login_url='login')
def tableRelease(request):
    employe = Employes.objects.get(employeeNumber=request.user)
    start = request.GET.get('fechaI')
    end = request.GET.get('fechaF')
    
    if 'bt-project' in request.POST: 
        if request.method == 'POST':
            employe.privileges = request.POST.get('bt-project')
            employe.save()
            return redirect('uut_form')
    
    if employe.privileges != 'SONY':
        return redirect('home')
    
    if start == None or end == None or start == '' or end == '':
        l1 = Release.objects.filter(shift='1')
        l2 = Release.objects.filter(shift='2')
        l3 = Release.objects.filter(shift='3')
        releases = Release.objects.all().count()
        
        fallasr = Failures.objects.filter(sn_f__pn_b__commodity='RACK').count()
        fallass = Failures.objects.filter(sn_f__pn_b__commodity='SLED').count()
        fallask = Failures.objects.filter(sn_f__pn_b__commodity='KURA').count()
        turno1 = Release.objects.filter(shift='1').count()
        turno2 = Release.objects.filter(shift='2').count()
        turno3 = Release.objects.filter(shift='3').count()
        
        causeD = int(Failures.objects.filter(rootCause='DEBUG').count())
        causeR = int(Failures.objects.filter(rootCause='RUTEO').count())
        causeP = int(Failures.objects.filter(rootCause='PRUEBAS').count())
        causeE = int(Failures.objects.filter(rootCause='ENSAMBLE').count())
        causeC = int(Failures.objects.filter(rootCause='CODIGO').count())
        causeF = int(Failures.objects.filter(rootCause='FUNCIONAL').count())
        
        t1 = int(Failures.objects.filter(id_s__stationName='INIT').count())
        t2 = int(Failures.objects.filter(id_s__stationName='FVT_POWERSHELF').count())
        t3 = int(Failures.objects.filter(id_s__stationName='PRE_FVT_COMPUTE_SLED').count())
        t4 = int(Failures.objects.filter(id_s__stationName='FVT_COMPUTE_SLED').count())
        t5 = int(Failures.objects.filter(id_s__stationName='STRESS (SLED)').count())
        t6 = int(Failures.objects.filter(id_s__stationName='STRESS (KURA)').count())
        t7 = int(Failures.objects.filter(id_s__stationName='FVT_RACK').count())
        t8 = int(Failures.objects.filter(id_s__stationName='FVT_STORAGE').count())
        t9 = int(Failures.objects.filter(id_s__stationName='FVT_COMPUTE_MODULE').count())
    else:
        datetime.strptime(start, '%Y-%m-%d').date()
        datetime.strptime(end, '%Y-%m-%d').date()
        l1 = Release.objects.filter(shift='1').filter(date__gte=start, date__lt=end)
        l2 = Release.objects.filter(shift='2').filter(date__gte=start, date__lt=end)
        l3 = Release.objects.filter(shift='3').filter(date__gte=start, date__lt=end)
        releases = Release.objects.filter(date__gte=start, date__lt=end).count()
        
        turno1 = Release.objects.filter(shift='1').filter(date__gte=start, date__lt=end).count()
        turno2 = Release.objects.filter(shift='2').filter(date__gte=start, date__lt=end).count()
        turno3 = Release.objects.filter(shift='3').filter(date__gte=start, date__lt=end).count()
        
        fallasr = Failures.objects.filter(sn_f__pn_b__commodity='Rack').filter(failureDate__gte=start, failureDate__lt=end).count()
        fallass = Failures.objects.filter(sn_f__pn_b__commodity='Sled').filter(failureDate__gte=start, failureDate__lt=end).count()
        fallask = Failures.objects.filter(sn_f__pn_b__commodity='Kura').filter(failureDate__gte=start, failureDate__lt=end).count()

        causeD = int(Failures.objects.filter(rootCause='DEBUG').filter(failureDate__gte=start, failureDate__lt=end).count())
        causeR = int(Failures.objects.filter(rootCause='RUTEO').filter(failureDate__gte=start, failureDate__lt=end).count())
        causeP = int(Failures.objects.filter(rootCause='PRUEBAS').filter(failureDate__gte=start, failureDate__lt=end).count())
        causeE = int(Failures.objects.filter(rootCause='ENSAMBLE').filter(failureDate__gte=start, failureDate__lt=end).count())
        causeC = int(Failures.objects.filter(rootCause='CODIGO').filter(failureDate__gte=start, failureDate__lt=end).count())
        causeF = int(Failures.objects.filter(rootCause='FUNCIONAL').filter(failureDate__gte=start, failureDate__lt=end).count())
        
        t1 = int(Failures.objects.filter(id_s__stationName='INIT').filter(failureDate__gte=start, failureDate__lt=end).count())
        t2 = int(Failures.objects.filter(id_s__stationName='FVT_POWERSHELF').filter(failureDate__gte=start, failureDate__lt=end).count())
        t3 = int(Failures.objects.filter(id_s__stationName='PRE_FVT_COMPUTE_SLED').filter(failureDate__gte=start, failureDate__lt=end).count())
        t4 = int(Failures.objects.filter(id_s__stationName='FVT_COMPUTE_SLED').filter(failureDate__gte=start, failureDate__lt=end).count())
        t5 = int(Failures.objects.filter(id_s__stationName='STRESS (SLED)').filter(failureDate__gte=start, failureDate__lt=end).count())
        t6 = int(Failures.objects.filter(id_s__stationName='STRESS (KURA)').filter(failureDate__gte=start, failureDate__lt=end).count())
        t7 = int(Failures.objects.filter(id_s__stationName='FVT_RACK').filter(failureDate__gte=start, failureDate__lt=end).count())
        t8 = int(Failures.objects.filter(id_s__stationName='FVT_STORAGE').filter(failureDate__gte=start, failureDate__lt=end).count())
        t9 = int(Failures.objects.filter(id_s__stationName='FVT_COMPUTE_MODULE').filter(failureDate__gte=start, failureDate__lt=end).count())
    
    labels_test = ['INIT', 'FVT_POWERSHELF', 'PRE_FVT_COMPUTE_SLED', 'FVT_COMPUTE_SLED', 'STRESS (SLED)', 'STRESS (KURA)', 'FVT_RACK', 'FVT_STORAGE', 'FVT_COMPUTE_MODULE']
    value_test = [t1,t2,t3,t4,t5,t6,t7,t8,t9]
    
    labels_cause = ['Debug', 'Ruteo', 'Pruebas', 'Ensamble', 'Codigo', 'Funcional']
    value_cause = [causeD, causeR, causeP, causeE, causeC, causeF]
    
    labels_rack = ['Rack liberados','Rack fallados']
    value_rack = [int(releases),int(fallasr)]  
    
    labels_sled = ['Sled liberados','Sled fallados']
    value_sled = [(int(releases)*12),int(fallass)]
    
    labels_kura = ['Kura liberados','Kura fallados']
    value_kura = [int(releases),int(fallask)]
    
    turnos = [int(turno1), int(turno2), int(turno3)]
    seriales = [l1, l2, l3]
    context = {'turnos':turnos,'employe':employe, 'labels_rack':labels_rack, 'value_rack':value_rack, 'labels_sled':labels_sled, 'value_sled':value_sled, 'labels_kura':labels_kura, 'value_kura':value_kura, 'labels_cause':labels_cause, 'value_cause':value_cause, 'labels_test':labels_test, 'value_test':value_test, 'seriales':seriales}
    return render(request=request, template_name='base/table_release.html', context=context)


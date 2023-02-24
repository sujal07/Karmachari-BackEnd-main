from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mainapp.models import *
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta, date
from django.views.decorators.csrf import csrf_exempt
from .forms import LeavesForm

# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required(login_url='login')
def home(request):
    fullname =  request.user.get_full_name()
    profile=Profile.objects.get(user=request.user)
    context = {'fullname':fullname,
               'profile':profile,
               'navbar':'home',
               }
    return render(request,'Home.html',context)


    
#login request gets value from action of html.login/form
def login(request):
    
    if request.user.is_authenticated:
         return redirect ('home')
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = auth.authenticate(username= username, password= password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Credentials Invalid")
            return redirect ('login')
    else:
        return render(request,'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def information(request):
      profile=Profile.objects.get(user=request.user)
      context={
      'profile':profile,
      'navbar':'yourinformation',
      
    }
      return render(request,'your_information.html',context)

@login_required(login_url='login')
def notice(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user_object)
    notices= Notice.objects.all()
    context={
        'profile':profile,
        'notices':notices,
        'navbar':'notice',
        
    }
    return render(request,'notices.html',context)

@login_required(login_url='login')
def attendance(request):
    user_object = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user_object)
    notices= Notice.objects.all()
    context={
        'profile':profile,
        'notices':notices,
        'navbar':'attendance',
        
    }
    return render(request,'attendance.html',context)
    
    

@csrf_exempt
def checkin(request):
    # if request.is_ajax():
    if request.method == 'POST':
        print("CHECK IN")
        user = request.user
        dateOfQuestion = datetime.today()
        checkInTime = timezone.now()
        Calendar.objects.create(user=user, checkInTime=checkInTime,dateOfQuestion=dateOfQuestion)
        return JsonResponse({'in_time': checkInTime})
    response = {'message': 'Success'}
    return JsonResponse(response)

@csrf_exempt
def checkout(request):
    # if request.is_ajax():
    if request.method == 'POST':
        print("CHECK OUT") 
        user = request.user
        checkOutTime = timezone.now()
        current_calendar = Calendar.objects.filter(user=user).latest('checkInTime')
        current_calendar.checkOutTime = checkOutTime
        current_calendar.save()
        duration = current_calendar.calculate_duration()

        # Get the schedule of the user's department
        profile = Profile.objects.get(user=request.user)
        department = profile.department.id
        schedule = Schedule.objects.get(department=department)
        late_time = datetime.combine(date.today(), schedule.schedule_start) + timedelta(minutes=15)
        late_time = late_time.time()


        # Determine the status based on the schedule and check-in time
        if current_calendar.checkInTime.time() > late_time:
            status = 'L'  # Late
        elif current_calendar.checkOutTime.time() < schedule.schedule_end:
            status = 'LV'  # Leave
        elif duration > (schedule.schedule_end - schedule.schedule_start).total_seconds() / 3600.0:
            status = 'A'  # Absent
        else:
            status = 'P'  # Presents

        # Create an Attendance object
        attendance = Attendance.objects.create(
            user=user,
            name=profile.user.get_full_name(),
            calendar=current_calendar,
            duration=duration,
            status=status,
        )

        return JsonResponse({'out_time': checkOutTime, 'duration': duration})
    response = {'message': 'Success'}
    return JsonResponse(response)





#####################################LEAVES############################################
@login_required(login_url='login')
def leaves(request):
    leaves= Leaves.objects.filter(user_id=request.user.id)
    submitted=False
    profile=Profile.objects.get(user=request.user)
    form = LeavesForm()
    if request.method == 'POST':
        form = LeavesForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user.id
            # Leaves = form.save(commit=False)
            # Leaves.user = request.user
            form.save()
            return HttpResponseRedirect('leaves?submitted=True')
    else:
        form=LeavesForm()
        if 'submitted in request.GET':
            submitted=True
            context={
            'profile':profile,
            # 'navbar':'leaves',
            'form': form,
            'submitted':submitted,
            'leaves':leaves,
            }
            return render(request,'leaves.html',context)


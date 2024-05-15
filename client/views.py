from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth, messages
from adminlawyer.models import *
from client.models import *
from datetime import date
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail


def hello(request):
    return HttpResponse("Hello, World!")

def profile(request,id):
    result = Client.objects.get(user_id=id)
    context = {'result':result}
    return render(request,'client/profile.html',context)

def layout(request):
    context = {}
    return render(request,'client/layout.html',context)

def about(request):
    context = {}
    return render(request,'client/about.html',context)

def feedback(request):
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(pk=id)
        cases = Cases.objects.all()
        client = Client.objects.all()
    else:
        return render(request,'client/login.html')

    context = {'cases':cases,'user':user,'client':client}
    return render(request,'client/feedback.html',context)


def cases(request):
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(pk=id)
        cases = Cases.objects.all()
        client = Client.objects.all()
    else:
        return render(request,'client/login.html')

    context = {'cases':cases,'user':user,'client':client}
    return render(request,'client/cases.html',context)

# def cases_store(request):
#     case_title  = request.POST['case_type']
#     message = request.POST['message']
#     court = request.POST['court']
#     judge = request.POST['judge']

#     ContactMessage.objects.create(case_type=case_type, message=message, court=court, judge=judge)
#     messages.success(request, 'Thank you for your valuable feedback!!')
#     return redirect('/client/cases')


def view_details(request,id):
    if request.user.is_authenticated:
        result  = Cases.objects.get(pk=id)
        dates = Schedule.objects.all()
        docs = Documents.objects.all()
    else:
        return render(request,'client/login.html')

    context = {'result':result,'dates':dates,'docs':docs}
    return render(request, 'client/view_details.html',context)

def appointment(request):
    if request.user.is_authenticated:
        id = request.user.id
        user = User.objects.get(pk=id)
        cases = Cases.objects.all()
        client = Client.objects.all()
    else:
        return render(request,'client/login.html')

    context = {'cases':cases,'user':user,'client':client}
    return render(request,'client/appointment.html',context)


def appointment_store(request):
    date    = request.POST['date']
    time    = request.POST['time']
    status  = "Pending"
    cases   = request.POST['case']
    subject = request.POST['subject']
    message = request.POST['message']

    id = request.user.id
    user = User.objects.get(pk=id)
    result = Client.objects.all()

    for res in result:
        if res.user_id == id:
            clientid = res.id

    Appointment.objects.create(date=date, time=time, status=status, subject=subject, message=message, cases_id=cases, client_id=clientid)
    messages.success(request, 'Appointment request sent successfully!!')
    return redirect('/client/appointment')


def header(request):
    context = {}
    return render(request,'client/header.html',context)

def sidebar(request):
    context = {}
    return render(request,'client/sidebar.html',context)

def footer(request):
    context = {}
    return render(request,'client/footer.html',context)

def home(request):
    context = {}
    return render(request,'client/home.html',context)


def login(request):
    context = {}
    return render(request,'client/login.html',context)


# def login_check(request):
#     username = request.POST['username']
#     password = request.POST['password']

#     result = auth.authenticate(request, username=username, password=password)

#     if result is None:
#         messages.success(request, 'Invalid Username Or Password!!')
#         return redirect('/client/login')
#     else:
#         auth.login(request, result)
#         return redirect('/client/home')

def login_check(request):
    username = request.POST['username']
    password = request.POST['password']

    result = auth.authenticate(request, username=username, password=password)

    if result is None:
        messages.success(request, 'Invalid Username Or Password!!')
        return redirect('/client/login')
    else:
        if Client.objects.filter(user_id=result.id).exists():
            auth.login(request, result)
            client = Client.objects.get(user_id=result.id)
            client_name = client.client_name
            # Pass the client_name to the template context
            request.session['client_name'] = client_name
            return redirect('/client/home')
        else:
            messages.info(request,'Inavlid Username or Password')
            return redirect('/client/login')


def logout(request):
    auth.logout(request)
    if 'client_name' in request.session:
        del request.session['client_name']
    return redirect('/client/home')


def feedback_store(request):
    today = datetime.today().strftime('%Y-%m-%d')
    date = today
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time = current_time
    case  = request.POST['case']
    rating  = request.POST['rating']
    message = request.POST['message']
    
    id = request.user.id
    user = User.objects.get(pk=id)
    result = Client.objects.all()

    for res in result:
        if res.user_id == id:
            clientid = res.id

    Feedback.objects.create(date=date, time=time, rating=rating,message=message, cases_id=case,client_id=clientid)
    messages.success(request, 'Thank you for your valuable feedback!!')
    return redirect('/client/feedback')

def contact(request):
    context = {}
    return render(request,'client/contact.html',context)

def contact_store(request):
    name  = request.POST['name']
    email  = request.POST['email']
    message = request.POST['messagecon']
    subject = request.POST['subject']

    ContactMessage.objects.create(name=name, email=email, message=message, subject=subject)
    messages.success(request, 'Thank you for your valuable feedback!!')
    return redirect('/client/contact')

def forgot(request):
    context = {}
    return render(request,'client/forgot_password.html',context)

def forgot_password(request):
	myemail = request.POST['email']

	if User.objects.filter(email=myemail).exists():
		result = User.objects.get(email=myemail)
		id = result.id
		client = Client.objects.get(user_id=id)
		password = client.password

		subject = 'Welcome to Case Tracker'
		message = f'Your Password is {password}'
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [myemail, ]

		send_mail( subject, message, email_from, recipient_list )
		return redirect('/client/login')


	else:
		messages.error(request,'Email not Found in Database')
		return redirect('/client/forgot')

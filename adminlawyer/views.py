from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
# from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from adminlawyer.models import *
import re, datetime
import urllib.request
import os
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from io import BytesIO
from .utils import generate_ics_file 
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
# import mysql.connector


def layout(request):
    context = {}
    return render(request,'adminlawyer/layout.html',context)

def profile(request,id):
    result = Lawyer.objects.get(user_id=id)
    context = {'result':result}
    return render(request,'adminlawyer/profile.html',context)

def header(request):
    context = {}
    return render(request,'adminlawyer/header.html',context)

def sidebar(request):
    context = {}
    return render(request,'adminlawyer/sidebar.html',context)

def footer(request):
    context = {}
    return render(request,'adminlawyer/footer.html',context)

def result(request,id):
    res  = Cases.objects.get(pk=id)
    context = {'res':res}
    return render(request,'adminlawyer/result.html',context)

def result_store(request,id):
    data = {
                'result'        : request.POST['result'],
                'status'       : request.POST['status'],
                'remarks'      : request.POST['remarks'],
           }
    Cases.objects.update_or_create(pk=id, defaults=data)
    result1 = Cases.objects.get(pk=id)
    res = result1.id
    return redirect(result, id=res)

from django.shortcuts import redirect
from django.core.mail import EmailMessage
from .models import Appointment, Client

# def accept_appointment(request, id):
#     appointment = Appointment.objects.get(pk=id)
#     client = Client.objects.get(pk=appointment.client_id)
    
#     # Update appointment status to "Approved"
#     appointment.status = "Approved"
#     appointment.save()
#     appointment.title = "Your Appointment to Meet Your lawyer"

#     # Generate calendar file content
#     cal_content = generate_ics_file(appointment.date, appointment.time, appointment.title)
    
#     # Create email message
#     subject = 'Appointment Approved'
#     d = appointment.date.strftime("%m/%d/%Y")
#     t = appointment.time.strftime("%H:%M:%S")
#     message = f'Your Appointment Request is Approved for {d} on {t}\nThank You!!'

#     # Add Google Calendar and Outlook Calendar links
#     google_calendar_link = f'https://www.google.com/calendar/render?action=TEMPLATE&text={appointment.title}&dates={appointment.date.strftime("%Y%m%dT%H%M%S")}/{appointment.date.strftime("%Y%m%dT%H%M%S")}'
#     outlook_calendar_link = f'https://outlook.live.com/calendar/0/deeplink/compose?subject={appointment.title}&startdt={appointment.date.strftime("%Y-%m-%d")}&enddt={appointment.date.strftime("%Y-%m-%d")}'

#     # Create email message with appointment details and calendar links
#     email = EmailMessage(
#         subject,
#         message,
#         'onlinelawyeroffice@gmail.com',
#         [client.email],
#     )
#     image_name = 'google.png'  # Replace 'your_image.jpg' with the actual image filename
#     image_path = os.path.join(settings.STATIC_ROOT, 'adminlawyer', 'images', image_name)
#     # google_logo_url = request.build_absolute_uri('/static/google.png')
#     # outlook_logo_url = request.build_absolute_uri('/static/outlook.png')
#     # Construct the HTML content for the email body
#     email_body = f'''
#     <p>Your Appointment Request is Approved for {d} on {t}. Thank you!</p>
#     <p>Click below links to add this event to your calendar:</p>
#     <p><a href="{google_calendar_link}"><img src="{image_path}" height="30px" width="30px" > Google Calander</a>&#160;
#     <a href="{outlook_calendar_link}"><img src="https://icons8.com/icon/WnHyYA2ecNqL/outlook-calendar"  ></a></p>
#     '''
#     email.content_subtype = "html"
#     email.body = email_body
    
#     # Send the email
#     email.send()
    
#     return redirect('view_appointment')

def accept_appointment(request, id):
    appointment = Appointment.objects.get(pk=id)
    client = Client.objects.get(pk=appointment.client_id)
    
    # Update appointment status to "Approved"
    appointment.status = "Approved"
    appointment.save()
    
    # Generate calendar file content
    cal_content = generate_ics_file(appointment.date, appointment.time, "Your Appointment to Meet Your lawyer")
    
    # Create email message
    subject = 'Appointment Approved'
    d = appointment.date.strftime("%m/%d/%Y")
    t = appointment.time.strftime("%H:%M:%S")
    message = f'Your Appointment Request is Approved for {d} on {t}\nThank You!!'
    appointment.title = 'Set Reminder To meet Your Lawyer'
    # Add Google Calendar and Outlook Calendar links
    google_calendar_link = f'https://www.google.com/calendar/render?action=TEMPLATE&text={appointment.title}&dates={appointment.date.strftime("%Y%m%dT%H%M%S")}/{appointment.date.strftime("%Y%m%dT%H%M%S")}'
    outlook_calendar_link = f'https://outlook.live.com/calendar/0/deeplink/compose?subject={appointment.title}&startdt={appointment.date.strftime("%Y-%m-%d")}&enddt={appointment.date.strftime("%Y-%m-%d")}'
    
    # Render email template
    email_body = render_to_string('adminlawyer/appointment_email_template.html', {
        'appointment': appointment,
        'google_calendar_link': google_calendar_link,
        'outlook_calendar_link': outlook_calendar_link,
    })

    # Create email message
    email = EmailMessage(
        subject=subject,
        body=email_body,
        from_email='onlinelawyeroffice@gmail.com',
        to=[client.email],
    )
    email.content_subtype = "html"

    # Send the email
    email.send()
    
    return redirect('view_appointment')

def reject_appointment(request,id):
    data = {
                'status' : "Rejected",
           }
    result = Appointment.objects.get(pk=id)
    us = Client.objects.get(pk=result.client_id)
    d = result.date.strftime("%m/%d/%Y")
    t = result.time.strftime("%H:%M:%S")
    message = 'Your Appointment Request is Rejected due to busy Schedule for ' + d + ' on ' + t + '\nPlease Make Another Appointment' + '\nThank You!!'
    email = EmailMessage(
            'Appointment Rejected',
            message,
            'onlinelawyeroffice@gmail.com',
            [us.email]
        )

        # Send the email
    email.send()
    Appointment.objects.update_or_create(pk=id, defaults=data)
    return redirect('/adminlawyer/view_appointment')

def taken_appointment(request,id):
    data = {
                'status' : "Taken",
           }
    Appointment.objects.update_or_create(pk=id, defaults=data)
    return redirect('/adminlawyer/view_appointment')

def dashboard(request):
    case  = Cases.objects.all().count()
    client = Client.objects.all().count()
    lawyer = Lawyer.objects.all().count()
    doc    = Documents.objects.all().count()
    app    = Appointment.objects.all().count()
    context = {'case':case,'client':client,'lawyer':lawyer,'doc':doc,'app':app}
    return render(request,'adminlawyer/dashboard.html',context)

def view_all_date(request):
    result = Schedule.objects.all()
    context = {'result':result}
    return render(request,'adminlawyer/view_all_date.html',context)

def table(request):
    context = {}
    return render(request,'adminlawyer/table.html',context)

def form(request):
    context = {}
    return render(request,'adminlawyer/form.html',context)

def calendar(request):
    context = {}
    return render(request,'adminlawyer/calendar.html',context)

def add_case(request):
    result = Client.objects.all()
    result1 = Lawyer.objects.all()
    state = State.objects.all()
    city  = City.objects.all()
    context = {'result':result,'result1':result1,'city':city,'state':state}
    return render(request,'adminlawyer/add_case.html',context)

def all_cases(request,id):
    result  = Cases.objects.get(pk=id)
    context = {'result':result}
    return render(request, 'adminlawyer/all_cases.html',context)

def detail_client(request,id):
    result  = Client.objects.get(pk=id)
    context = {'result':result}
    return render(request, 'adminlawyer/detail_client.html',context)

def detail_member(request,id):
    result  = Lawyer.objects.get(pk=id)
    context = {'result':result}
    return render(request, 'adminlawyer/detail_member.html',context)


def search_case(request):
    title1    = request.POST['title']
    result1 = Cases.objects.filter(title__icontains=title1).count()
    if result1 is not 0:
        result = Cases.objects.filter(title__icontains=title1)
    else:
        result = 0
    context = {'result':result,'result1':result1}
    return render(request,'adminlawyer/search_case.html',context)

def view_doc(request,id):
    case  = Cases.objects.get(pk=id)
    result = Documents.objects.all()
    context = {'case':case,'result':result}
    return render(request, 'adminlawyer/view_doc.html',context)

def view_date(request,id):
    case  = Cases.objects.get(pk=id)
    result = Schedule.objects.all()
    context = {'case':case,'result':result}
    return render(request,'adminlawyer/view_date.html',context)

def add_client(request):
    state = State.objects.all()
    city  = City.objects.all()
    context = {'city':city,'state':state}
    return render(request,'adminlawyer/add_client.html',context)

def add_doc(request):
    context = {}
    return render(request,'adminlawyer/add_doc.html',context)

def add_member(request):
    state = State.objects.all()
    city  = City.objects.all()
    context = {'city':city,'state':state}
    return render(request,'adminlawyer/add_member.html',context)

def view_cases(request):
    result = Cases.objects.all()
    result1 = Lawyer.objects.all()
    context = {'result':result,'result1':result1}
    return render(request,'adminlawyer/view_cases.html',context)

def view_client(request):
    result = Client.objects.all()
    context = {'result':result}
    return render(request, 'adminlawyer/view_client.html',context)

def view_member(request):
    result = Lawyer.objects.all()
    context = {'result':result}
    return render(request,'adminlawyer/view_member.html',context)

def view_feedback(request):
    result = Feedback.objects.all().order_by('date')
    context = {'result':result}
    return render(request,'adminlawyer/view_feedback.html',context)

def view_appointment(request):
    result = Appointment.objects.filter(status="Pending")
    approved = Appointment.objects.filter(status="Approved").order_by('date')
    context = {'result':result,'approved':approved}
    return render(request,'adminlawyer/view_appointment.html',context)
    
def login(request):
    context = {}
    return render(request,'adminlawyer/login.html',context)


def lawyer_store(request):
    username    = request.POST['username']
    email = request.POST['email']
    lawyer_name = request.POST['lawyer_name']
    password = request.POST['password']
    dob = request.POST['dob']
    d = dob.split("-")
    today = date.today()
    year = int(d[0])
    month = int(d[1])
    day = int(d[2])
    age = today.year - year - ((today.month, today.day) < (month, day))
    gender = request.POST['gender']
    contact = request.POST['contact']
    qualification = request.POST['qualification']
    experience = request.POST['experience']
    registration_date = request.POST['registration_date']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    photo = request.FILES['photo']
    mylocation = os.path.join(settings.MEDIA_ROOT, 'staff')
    obj = FileSystemStorage(location=mylocation)
    obj.save(photo.name, photo)

    result = User.objects.create_user(email=email,username=username,password=password,first_name=lawyer_name,last_name=photo.name)
    Lawyer.objects.create(qualification = qualification, experience = experience, registration_date = registration_date, photo = photo.name, username = username, lawyer_name = lawyer_name, email = email, address = address, contact = contact, password = password, dob = dob, age = age, gender = gender, city_id = city, state_id = state, zipcode = zipcode,user_id=result.id)
    us = Lawyer.objects.get(username=username)
    u = us.username
    e = us.email
    p = us.password
    message = 'Your Account is Created, here is information for you to login\n\n' + 'Username : ' + u + '\nEmail : ' + e + '\nPassword : ' + p + '\n\nPlease do not share this information with anyone.' + '\n\nThank You!!'
    email = EmailMessage(
            'Account Information',
            message,
            'onlinelawyeroffice@gmail.com',
            [us.email]
        )
        # Send the email
    email.send()
    return redirect('/adminlawyer/add_member')

def login_check(request):
    username = request.POST['username']
    password = request.POST['password']

    result = auth.authenticate(request, username=username, password=password)
    print(result)

    if result is None:
        print('Invalid Username Or Password')
        return redirect('/adminlawyer/login')
    else:
        if Lawyer.objects.filter(user_id=result.id).exists() and result.is_superuser == 1:
            auth.login(request, result)
            return redirect('/adminlawyer/dashboard')
        else:
            messages.info(request,'Inavlid Username or Password')
            return redirect('/adminlawyer/login')
            


def logout(request):
    auth.logout(request)
    return redirect('/adminlawyer/login')


def client_store(request):
    username    = request.POST['username']
    email = request.POST['email']
    client_name = request.POST['client_name']
    password = request.POST['password']
    dob = request.POST['dob']
    d = dob.split("-")
    today = date.today()
    year = int(d[0])
    month = int(d[1])
    day = int(d[2])
    age = today.year - year - ((today.month, today.day) < (month, day))
    gender = request.POST['gender']
    contact = request.POST['contact']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    photo = request.FILES['photo']
    mylocation = os.path.join(settings.MEDIA_ROOT, 'client')
    obj = FileSystemStorage(location=mylocation)
    obj.save(photo.name, photo)

    result = User.objects.create_user(email=email,username=username,password=password,first_name=client_name,last_name=photo.name)
    Client.objects.create(photo = photo.name, username = username, client_name = client_name, email = email, address = address, contact = contact, password = password, dob = dob, age = age, gender = gender, city_id = city, state_id = state, zipcode = zipcode,user_id=result.id)
    us = Client.objects.get(username=username)
    u = us.username
    e = us.email
    p = us.password
    message = 'Your Account is Created, here is information for you to login\n\n' + 'Username : ' + u + '\nEmail : ' + e + '\nPassword : ' + p + '\n\nPlease do not share this information with anyone.' + '\n\nThank You!!'
    email = EmailMessage(
            'Account Information',
            message,
            'onlinelawyeroffice@gmail.com',
            [us.email]
        )

        # Send the email
    email.send()
    return redirect('/adminlawyer/add_client')


def client_update(request,id):
    if len(request.FILES)!=0:
        photo = request.FILES['p']
        mylocation = os.path.join(settings.MEDIA_ROOT, 'client')
        obj = FileSystemStorage(location=mylocation)
        obj.save(photo.name, photo)
        photo = photo.name
    else:
        result = Cases.objects.get(pk=id)
        photo = result.photo

    data = {
                'photo' : photo,
                'client_name'        : request.POST['client_name'],
                'username'        : request.POST['username'],
                'email'       : request.POST['email'],
                'password'       : request.POST['password'],
                'dob'       : request.POST['dob'],
                # 'age' : request.POST['age'],
                'gender'       : request.POST['gender'],
                'address'      : request.POST['address'],
                'contact' : request.POST['contact'],
                'city_id'     : request.POST['city'],
                'state_id'         : request.POST['state'],
                'zipcode'     : request.POST['zipcode'],
                
           }
    data1 = {
                'username'        : request.POST['username'],
                'email'       : request.POST['email'],
                'last_name' : photo,
                'first_name'        : request.POST['client_name'],
    }
    result = Client.objects.get(pk=id)
    result1 = result.user_id
    pass1 = request.POST['password']
    Client.objects.update_or_create(pk=id, defaults=data)
    User.objects.update_or_create(pk=result1, defaults=data1)
    user = User.objects.get(pk=result1)
    user.set_password(pass1)
    user.save()
    return redirect('/adminlawyer/view_client')


def lawyer_update(request,id):
    if len(request.FILES)!=0:
        photo = request.FILES['photo']
        mylocation = os.path.join(settings.MEDIA_ROOT, 'staff')
        obj = FileSystemStorage(location=mylocation)
        obj.save(photo.name, photo)
        photo = photo.name
    else:
        result = Cases.objects.get(pk=id)
        photo = result.photo

    data = {
                'photo' : photo,
                'lawyer_name'        : request.POST['lawyer_name'],
                'username'        : request.POST['username'],
                'email'       : request.POST['email'],
                'password'       : request.POST['password'],
                'dob'       : request.POST['dob'],
                # 'age' : request.POST['age'],
                'gender'       : request.POST['gender'],
                'qualification'       : request.POST['qualification'],
                'experience'       : request.POST['experience'],
                'registration_date'       : request.POST['registration_date'],
                'address'      : request.POST['address'],
                'contact' : request.POST['contact'],
                'city_id'     : request.POST['city'],
                'state_id'         : request.POST['state'],
                'zipcode'     : request.POST['zipcode'],
                
           }
    data1 = {
                'username'        : request.POST['username'],
                'email'       : request.POST['email'],
                'last_name' : photo,
                'first_name'        : request.POST['lawyer_name'],
    }
    result = Lawyer.objects.get(pk=id)
    result1 = result.user_id
    pass1 = request.POST['password']
    Lawyer.objects.update_or_create(pk=id, defaults=data)
    User.objects.update_or_create(pk=result1, defaults=data1)
    user = User.objects.get(pk=result1)
    user.set_password(pass1)
    user.save()
    
    return redirect('/adminlawyer/view_member')


def case_store(request):
    title    = request.POST['title']
    description = request.POST['description']
    police_station = request.POST['police_station']
    case_type = request.POST['case_type']
    case_reg_date = request.POST['case_reg_date']
    court = request.POST['court']
    judge = request.POST['judge']
    status = request.POST['status']
    city = request.POST['city']
    state = request.POST['state']
    client = request.POST['client']
    lawyer = request.POST['lawyer']
    fir_copy = request.FILES['fir_copy']
    mylocation = os.path.join(settings.MEDIA_ROOT, 'document')
    obj = FileSystemStorage(location=mylocation)
    obj.save(fir_copy.name, fir_copy)

    Cases.objects.create(fir_copy = fir_copy.name, title = title, description = description, police_station = police_station, case_type = case_type, case_reg_date = case_reg_date, court = court, judge = judge, status = status, client_id = client, lawyer_id = lawyer, city_id = city, state_id = state)
    return redirect('/adminlawyer/add_case')



def case_update(request,id):
    if len(request.FILES)!=0:
        fir_copy = request.FILES['fir_copy']
        mylocation = os.path.join(settings.MEDIA_ROOT, 'document')
        obj = FileSystemStorage(location=mylocation)
        obj.save(fir_copy.name, fir_copy)
        fir_copy = fir_copy.name
    else:
        result = Cases.objects.get(pk=id)
        fir_copy = result.fir_copy

    data = {
                'title'        : request.POST['title'],
                'description'       : request.POST['description'],
                'police_station'      : request.POST['police_station'],
                'case_type' : request.POST['case_type'],
                'case_reg_date'     : request.POST['case_reg_date'],
                'court'            : request.POST['court'],
                'judge'     : request.POST['judge'],
                'status'     : request.POST['status'],
                'city_id'     : request.POST['city'],
                'state_id'     : request.POST['state'],
                'client_id'     : request.POST['client'],
                'lawyer_id'     : request.POST['lawyer'],
                'fir_copy'     : fir_copy,
           }
    Cases.objects.update_or_create(pk=id, defaults=data)
    return redirect('/adminlawyer/view_cases')

def view(request):
    pass


def client_delete(request,id):
    result = Client.objects.get(pk=id)
    result1 = User.objects.get(pk=result.user_id)
    result.delete()
    result1.delete()
    return redirect('/adminlawyer/view_client')


def lawyer_delete(request,id):
    result = Lawyer.objects.get(pk=id)
    result1 = User.objects.get(pk=result.user_id)
    result.delete()
    result1.delete()
    return redirect('/adminlawyer/view_member')


def case_delete(request,id):
    result = Cases.objects.get(pk=id)
    result.delete()
    return redirect('/adminlawyer/view_cases')

def document_delete(request,id):
    result1 = Documents.objects.get(pk=id)
    result = result1.cases_id
    result1.delete()
    return redirect(view_doc, id=result)

def date_delete(request,id):
    result1 = Schedule.objects.get(pk=id)
    result = result1.cases_id
    result1.delete()
    return redirect('/adminlawyer/view_all_date')

def client_edit(request,id):
    result  = Client.objects.get(pk=id)
    city = City.objects.all()
    state = State.objects.all()
    context = {'result':result,'city':city,'state':state}
    return render(request, 'adminlawyer/update_client.html',context)


def lawyer_edit(request,id):
    result  = Lawyer.objects.get(pk=id)
    city = City.objects.all()
    state = State.objects.all()
    context = {'result':result,'city':city,'state':state}
    return render(request, 'adminlawyer/update_member.html',context)


def case_edit(request,id):
    result  = Cases.objects.get(pk=id)
    lawyer = Lawyer.objects.all()
    client = Client.objects.all()
    city = City.objects.all()
    state = State.objects.all()
    context = {'result':result,'city':city,'state':state,'lawyer':lawyer,'client':client}
    return render(request, 'adminlawyer/update_case.html',context)

def index(request):
    context = {}
    return render(request, 'adminlawyer/index.html',context)











# connector

    # try:
    #     connection = mysql.connector.connect(host='localhost',
    #                                          database='lawyeroffice',
    #                                          user='root',
    #                                          password='')

    #     sql_select_Query = "select * from client where id=3"
    #     cursor = connection.cursor()
    #     cursor.execute(sql_select_Query)
    #     # get all records
    #     records = cursor.fetchall()
    #     print("Total number of rows in table: ", cursor.rowcount)

    #     # print("\nPrinting each row")
    #     for row in records:
    #         print("Id = ", row[0], )
    #         print("Name = ", row[1])
    #         # print("Price  = ", row[2])
    #         # print("Purchase date  = ", row[3], "\n")

    # except mysql.connector.Error as e:
    #     print("Error reading data from MySQL table", e)
    # finally:
    #     if connection.is_connected():
    #         connection.close()
    #         cursor.close()
    #         print("MySQL connection is closed")
    
def register_superuser(request):
    state = State.objects.all()
    city  = City.objects.all()
    context = {'city':city,'state':state}
    return render(request,'adminlawyer/add_lawyer.html',context)
    

def lawyer_store_super(request):
    username    = request.POST['username']
    email = request.POST['email']
    lawyer_name = request.POST['lawyer_name']
    password = request.POST['password']
    dob = request.POST['dob']
    d = dob.split("-")
    today = date.today()
    year = int(d[0])
    month = int(d[1])
    day = int(d[2])
    age = today.year - year - ((today.month, today.day) < (month, day))
    gender = request.POST['gender']
    contact = request.POST['contact']
    qualification = request.POST['qualification']
    experience = request.POST['experience']
    registration_date = request.POST['registration_date']
    address = request.POST['address']
    city = request.POST['city']
    state = request.POST['state']
    zipcode = request.POST['zipcode']
    photo = request.FILES['photo']
    mylocation = os.path.join(settings.MEDIA_ROOT, 'staff')
    obj = FileSystemStorage(location=mylocation)
    obj.save(photo.name, photo)

    result = User.objects.create_superuser(email=email,username=username,password=password,first_name=lawyer_name,last_name=photo.name)
    Lawyer.objects.create(qualification = qualification, experience = experience, registration_date = registration_date, photo = photo.name, username = username, lawyer_name = lawyer_name, email = email, address = address, contact = contact, password = password, dob = dob, age = age, gender = gender, city_id = city, state_id = state, zipcode = zipcode,user_id=result.id)
    us = Lawyer.objects.get(username=username)
    u = us.username
    e = us.email
    p = us.password
    message = 'Your Account is Created, here is information for you to login\n\n' + 'Username : ' + u + '\nEmail : ' + e + '\nPassword : ' + p + '\n\nPlease do not share this information with anyone.' + '\n\nThank You!!'
    email = EmailMessage(
            'Account Information',
            message,
            'onlinelawyeroffice@gmail.com',
            [us.email]
        )
        # Send the email
    email.send()
    return redirect('/adminlawyer/login')

# client Reads---
def client_list(request):
    clients = Client.objects.select_related('user').all()  # Join Client with auth_user
    return render(request, 'adminlawyer/client_list.html', {'clients': clients})
def delete_client(request, client_id):
    if request.method == 'POST':
        client = get_object_or_404(Client, pk=client_id)
        
        # Retrieve cases associated with the client
        client_cases = Cases.objects.filter(client=client)
        
        # Retrieve appointments related to the client's cases
        appointments = Appointment.objects.filter(cases__in=client_cases)
        
        # Retrieve documents related to the client's cases
        documents = Documents.objects.filter(cases__in=client_cases)
        
        # Retrieve feedback related to the client's cases
        feedbacks = Feedback.objects.filter(cases__in=client_cases)
        
        # Delete feedback associated with the client's cases
        feedbacks.delete()
        
        # Delete documents associated with the client's cases
        documents.delete()
        
        # Delete appointments associated with the client's cases
        appointments.delete()
        
        # Delete associated user (cascades deletion to related records)
        client.user.delete()
        # Client is deleted automatically due to on_delete=models.CASCADE
        
        return redirect('/adminlawyer/client_list')
    else:
        # Handle non-POST requests (if necessary)
        pass


def lawyer_list(request):
    lawyers = Lawyer.objects.select_related('user').all()  # Join Lawyer with auth_user
    return render(request, 'adminlawyer/lawyer_list.html', {'lawyers': lawyers})


def delete_lawyer(request, lawyer_id):
    if request.method == 'POST':
        lawyer = get_object_or_404(Lawyer, pk=lawyer_id)
        
        # Retrieve cases associated with the lawyer
        lawyer_cases = Cases.objects.filter(lawyer=lawyer)
        
        # Retrieve related feedback
        lawyer_feedbacks = Feedback.objects.filter(cases__in=lawyer_cases)
        
        # Retrieve related documents
        lawyer_documents = Documents.objects.filter(cases__in=lawyer_cases)
        
        # Retrieve related appointments
        lawyer_appointments = Appointment.objects.filter(cases__in=lawyer_cases)
        
        # Retrieve related schedules
        lawyer_schedules = Schedule.objects.filter(cases__in=lawyer_cases)
        
        # Delete associated schedules
        lawyer_schedules.delete()
        
        # Delete associated feedback
        lawyer_feedbacks.delete()
        
        # Delete associated documents
        lawyer_documents.delete()
        
        # Delete associated appointments
        lawyer_appointments.delete()
        
        # Delete associated cases
        lawyer_cases.delete()
        
        # Delete associated user
        lawyer.user.delete()
        
        # Delete lawyer
        lawyer.delete()
        
        return redirect('/adminlawyer/lawyer_list')
    else:
        # Handle non-POST requests (if necessary)
        pass
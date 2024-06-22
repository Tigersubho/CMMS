from django.db.models import Q
from django.shortcuts import render, redirect
from .models import User, Ticket
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , JsonResponse






def loginuser(request):
    return render(request, 'app/loginuser.html')

def loginhandler(request):
    return render(request, 'app/loginhandler.html')

def loginadmin(request):
    return render(request, 'app/loginadmin.html')

def usertable(request):
    return render(request, 'app/usertable.html')



def loginsuperadmin(request):
    return render(request, 'app/loginsuperadmin.html')

def index(request):
    return render(request, 'app/index.html')

def superadmin(request):
    UID = request.user.UID
    try:
        name = User.objects.get(UID=UID)
    except User.DoesNotExist:
        name = "USER"

    ticket = Ticket.objects.all()
    context = {'ticket': ticket , 'name':name}
    return render(request, 'app/superadmin.html' , context)

def admin(request):
    UID = request.user.UID
    try:
        user = User.objects.get(UID=UID)
    except User.DoesNotExist:
        user = None

    if user is None:
        return HttpResponse("User not found")


    if user.is_SYSadmin:
        ticket = Ticket.objects.filter(Q(HID="HID_SYS") | Q(HID__isnull=True))
    elif user.is_GMAadmin:
        ticket = Ticket.objects.exclude(HID="HID_SYS")
    else:
        return HttpResponse("Invalid admin type")

    context = {'ticket': ticket, 'name': user}
    return render(request, 'app/admin.html', context)



@login_required
def user(request):
    UID = request.user.UID
    try:
        name = User.objects.get(UID=UID)


    except User.DoesNotExist:
        name = "USER"

    # Fetch tickets associated with the user based on UID
    try:
        uid = Ticket.objects.filter(UID=UID)
    except Ticket.DoesNotExist:
        uid = []

    context = {'name': name, 'uid': uid}
    return render(request, 'app/user.html', context)


@login_required
def handler(request):
    email = request.user.email

    try:
        name = User.objects.get(email=email)
        HID = name.HID
        hid = Ticket.objects.filter(HID=HID)
    except User.DoesNotExist:
        name = None
        hid = []
    context = {'name': name, 'hid': hid}
    return render(request, 'app/handler.html', context)


def signuppageuser(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        dept = request.POST.get('department')
        school = request.POST.get('school')
        user_type = request.POST.get("user_type") 
        latest_user = User.objects.last()
        facility = request.POST.get('facility')

        if user_type == "customer":
            if latest_user and latest_user.UID:
                try:
                    n = int(latest_user.UID[3:]) + 1
                except ValueError:
                    n = 1
            else:
                n = 1
            num_digits = len(str(n))
            UID = f'UID{"0" * (2 - num_digits)}{n}'
            my_user = User.objects.create_user(UID=UID,school = school, dept = dept ,username=name, name=name, email=email, password=password,
                                               is_customer=True)
            my_user.save()
        elif user_type == "employee":
            if latest_user  and latest_user.UID:
                try:
                    n1 = int(latest_user.UID[3:]) + 1
                except ValueError:
                    n1 =1
            else:
                n1 =1
            num_digits1 = len(str(n1))

            fac = facility[:3].upper()
            HID = f'HID_{fac}'
            UID = f'UID{"0" * (2 - num_digits1)}{n1}'
            my_user = User.objects.create_user(UID= UID ,facility = facility,name =name,  username=name, hname=name, email=email, password=password,
                                               is_employee=True, HID=HID)

        elif user_type == "GMAadmin":
            if latest_user and latest_user.UID:
                try:
                    n = int(latest_user.UID[3:]) + 1
                except ValueError:
                    n = 1
            else:
                n = 1
            num_digits = len(str(n))
            UID = f'UID{"0" * (2 - num_digits)}{n}'
            my_user = User.objects.create_user(UID = UID , username=name, name=name, email=email, password=password, is_GMAadmin=True)
        
        elif user_type == "SYSadmin":
            if latest_user and latest_user.UID:
                try:
                    n = int(latest_user.UID[3:]) + 1
                except ValueError:
                    n = 1
            else:
                n = 1
            num_digits = len(str(n))
            UID = f'UID{"0" * (2 - num_digits)}{n}'
            my_user = User.objects.create_user(UID = UID , username=name, name=name, email=email, password=password, is_SYSadmin=True)
        
        elif user_type == "superadmin":
            if latest_user and latest_user.UID:
                try:
                    n = int(latest_user.UID[3:]) + 1
                except ValueError:
                    n = 1
            else:
                n = 1
            num_digits = len(str(n))
            UID = f'UID{"0" * (2 - num_digits)}{n}'
            my_user = User.objects.create_user(UID = UID , username=name, name=name, email=email, password=password, is_superadmin=True)

        else:
            print("hi")
            return redirect('/error')  # Handle invalid user types here

        my_user.save()
        return redirect('/loginadmin')
    return render(request, 'app/loginuser.html')


def loginpageuser(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = User.authenticate(request, email=email, password=password)
        print(user.password, password, email, user.email)

        if user is not None:
            login(request, user)
            if user.is_customer:
                return redirect('/user')  # Replace with your customer dashboard URL
            elif user.is_employee:
                return redirect('/handler')  # Replace with your employee dashboard URL
            elif user.is_SYSadmin:
                return redirect('/admin') 
            elif user.is_GMAadmin:
                return redirect('/admin')
            elif user.is_superadmin:
                return redirect('/superadmin') # Replace with your admin dashboard URL
        else:
            # User authentication failed, render an error page
            return render(request, 'app/error1.html')

    return render(request, 'app/error.html')  # Render an error page for GET requests


def UserLoggedIn(request):
    if request.user.is_authenticated:
        email = request.user.email
    else:
        email = None
    return email


def logout_view(request):
    email = UserLoggedIn(request)
    if email is not None:
        logout(request)
        return redirect('/')



    else:
        return HttpResponse("you must login first to logout")


# logics--------------------------------------------------------------

from django.core.mail import send_mail
from twilio.rest import Client
from django.conf import settings
from django.shortcuts import redirect



def TicketMS(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        facility = request.POST.get('facilities')
        fac = facility[:3].upper()
        HID = f'HID_{fac}'
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        email = request.user.email
        data = User.objects.get(email=email)
        UID = data.UID
        dept = data.dept
        users_with_hid = User.objects.filter(HID=HID)


        # Create a ticket for the first handler
        for user in users_with_hid:
            hname = user.hname
            email_recipient = user.email
            handler_ticket = create_ticket(facility, title, desc,hname, name, HID, UID, dept)
            send_notification(handler_ticket, email_recipient)
            send_confirmation(handler_ticket, email)
        return redirect('/user')
    else:
        print("Error: Could not save ticket")


def create_ticket(facility, title, desc,hname, name,HID, UID, dept):
    # Create a new ticket
    latest_user = Ticket.objects.last()
    if latest_user and latest_user.TID:
        try:
            n = int(latest_user.TID[3:]) + 1
        except ValueError:
            n = 1
    else:
        n = 1
    num_digits = len(str(n))
    TID = f'TID{"0" * (2 - num_digits)}{n}'

    # Create the ticket record
    ticket = Ticket(TID=TID, facilities=facility, dept=dept, uname=name, hname=hname , HID=HID, title=title,
                    description=desc, UID=UID)
    ticket.save()

    return ticket


def send_notification(ticket, email_recipient):
    # Compose the email message for the handler
    subject = f'Ticket Allocation: #{ticket.TID} - {ticket.title}'
    message = f'''
        Hello Handler,

        You have been assigned a new ticket with the following details:

        Ticket ID: {ticket.TID}
        Name of Issuer: {ticket.uname}
        Dept. of Issuer: {ticket.dept}
        Title: {ticket.title}
        Description: {ticket.description}
        Date: {ticket.created_at}

        Please take appropriate action and resolve it within 24 hours.

        Regards,
        Your Application Team
    '''

    # Send the email notification
    from_email = 'souvikghoshkalna3@gmail.com'
    send_mail(subject, message, from_email, [email_recipient])


def send_confirmation(ticket, email_recipient):
    # Compose the confirmation email message for the user
    confirmation_subject = f'Ticket Allocation: #{ticket.TID} - {ticket.title}'
    confirmation_message = f'''
        Hello User,

        Your ticket has reached us, and we will look
        into it shortly:
        Ticket ID: {ticket.TID}
        Handler Name: {ticket.hname}
        Title: {ticket.title}
        Description: {ticket.description}
        Date: {ticket.created_at}

        We would surely try and resolve it within 24 hours and
        will update you.
        Thank you for reaching out to us; hope you would
        like our service

        Regards,
        {ticket.hname}
    '''
    from_email = 'souvikghoshkalna3@gmail.com'
    # Send the confirmation email to the user who submitted the ticket
    send_mail(confirmation_subject, confirmation_message, from_email, [email_recipient])


def get_ticket_details(request, tid):
    try:
        # Retrieve the ticket details based on the provided TID
        ticket = Ticket.objects.get(TID=tid)
        # Serialize the ticket details into JSON format
        ticket_details = {
            'title': ticket.title,
            'description': ticket.description,
            # Include other ticket details here as needed
        }
        # Return the JSON response with ticket details
        return JsonResponse(ticket_details)
    except Ticket.DoesNotExist:
        # Handle the case where the ticket with the provided TID does not exist
        return JsonResponse({'error': 'Ticket not found'}, status=404)


def status(request):
    if request.method == "POST":
        TID = request.POST.get("TID").strip()

        response = request.POST.get("remark")
        status = request.POST.get('status')
        if status == 'a':
            send = 'Passed'
        elif status == 'b':
            send = 'In progress'
        elif status == 'c':
            send = 'Completed'
        elif status == 'd':
            send = 'Pending'
        time = request.POST.get('time')
        check = Ticket.objects.filter(TID=TID)
        if check is not None:
            if send == 'Completed':
                ticket = Ticket.objects.get(TID=TID)
                ticket.hreason = response
                ticket.status = send
                ticket.time = time
                ticket.save()
                UID = ticket.UID
                em1 = User.objects.get(UID=UID)
                subject1 = f'Ticket Status: #{ticket.TID} - {ticket.title}'
                message1 = f'''
                                        Hello User,

                                       You ticket issue has been solved .
                                        Ticket ID: {ticket.TID}
                                       Hadler Name: {ticket.hname}
                                        Title: {ticket.title}
                                       Description: {ticket.description}
                                        Date: {ticket.created_at}

                                       Thank you for reaching out to me hope you would like our service
                                        Regards,
                                       {ticket.hname}
                                        '''
                from_email = 'souvikghoshkalna3@gmail.com'

                emailid2 = em1.email
                recipient_list1 = [emailid2]
                send_mail(subject1, message1, from_email, recipient_list1)
                return redirect('/handler')
            elif send == 'In progress'  or send == 'Pending':
                ticket = Ticket.objects.get(TID=TID)
                ticket.hreason = response
                ticket.status = send
                ticket.time = time
                ticket.save()
                UID = ticket.UID
                em1 = User.objects.get(UID=UID)
                subject1 = f'Ticket Status: #{ticket.TID} - {ticket.title}'
                message1 = f'''
                                        Hello User,

                                       You ticket has been considered and this is the update:
                                        Ticket ID: {ticket.TID}
                                       Hadler Name: {ticket.hname}
                                        Title: {ticket.title}
                                       Description: {ticket.description}
                                        Date: {ticket.created_at}

                                        We have started working on this and it will probably be resolved within {ticket.time} hours.
                                       Remark : {ticket.hreason}

                                       Thank you for reaching out to me hope you would like our service
                                        Regards,
                                       {ticket.hname}
                                        '''
                from_email = 'souvikghoshkalna3@gmail.com'

                emailid2 = em1.email
                recipient_list1 = [emailid2]
                send_mail(subject1, message1, from_email, recipient_list1)
                return redirect('/handler')
            elif send == "Passed":
                ticket = Ticket.objects.get(TID=TID)
                ticket.delete()
                return redirect('/handler')

            else:
                print("hi")
                return redirect('/error')

        else:
            print("hello")
            return HttpResponse('/error')



from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter

def download(request):
    if request.method == 'POST':
        filter_value = request.POST.get('filter')

        # Replace 'Ticket.objects.filter()' with your actual query based on the filter
        if filter_value == 'all':
            tickets = Ticket.objects.all()
        elif filter_value == 'received':
            tickets = Ticket.objects.filter(status='Received')
        elif filter_value == 'On Going':
            tickets = Ticket.objects.filter(status='On Going')
        elif filter_value == 'Pending':
            tickets = Ticket.objects.filter(status='Pending')
        elif filter_value == 'Completed':
            tickets = Ticket.objects.filter(status='Completed')
        else:
            tickets = Ticket.objects.none()  # Handle invalid filter value

        # Create a PDF using ReportLab
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # Customize the PDF content with a table
        data = []
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header padding
            ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),  # Table data background color
            ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Table grid lines
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Data font
            ('BACKGROUND', (0, 1), (-1, 1), (0.8, 0.8, 0.8)),  # Header row background color
            ('LINEABOVE', (0, 0), (-1, 0), 1, (0, 0, 0)),  # Line above header
            ('LINEBELOW', (0, 0), (-1, 0), 1, (0, 0, 0)),  # Line below header
        ])

        # Header row
        header = ["Ticket ID", "Title", "Issuer", "Status", "Handler Reason", "Time", "Created At", "Facilities", "User ID", "Handler ID"]
        data.append(header)

        # Add ticket details to the table
        for ticket in tickets:
            row = [
                ticket.TID,
                ticket.title,
                ticket.uname,
                ticket.status,
                ticket.hreason,
                ticket.time,
                ticket.created_at,
                ticket.facilities,
                ticket.UID,
                ticket.HID,
            ]
            data.append(row)

        # Create the table and apply the table style
        ticket_table = Table(data)
        ticket_table.setStyle(table_style)

        # Add the table to the PDF elements
        elements.append(ticket_table)

        # Build the PDF
        doc.build(elements)

        # Set up the response and return the PDF for download
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="ticket_details.pdf"'

        return response
    else:
        # Handle GET request or other methods
        return render(request, 'your_template.html')


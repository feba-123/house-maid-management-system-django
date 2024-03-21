from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseForbidden
from .models import Service_Category
from .models import *
from .forms import HousemaidStatusUpdateForm
from .models import House_Resident, Flat_Resident
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import House_Resident, Housemaid, Order, Status,Contact
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
def home(request):
    services = Service_Category.objects.all()
    return render(request,'home.html',{'services':services})

def services_view(request):
    services = Service_Category.objects.all()
    return render(request, 'home.html', {'services': services})




def Login_User(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_houseresident:
                login(request, user)
                return redirect('siteusers:house_resident')  # Redirect to the home page for house residents
            elif user.is_flatresident:
                login(request, user)
                return redirect('siteusers:flat_resident')  # Redirect to the home page for normal users
            elif user.is_housemaid:
                housemaid = Housemaid.objects.filter(user=user).first()

                if housemaid:
                    if housemaid.status and housemaid.status.status == 'Approve':
                        login(request, user)
                        return redirect('siteusers:housemaid_home')  # Redirect to the home page for housemaids with approved status
                    elif housemaid.status and housemaid.status.status == 'pending':
                        return render(request, 'pending_alert.html')
                    elif housemaid.status and housemaid.status.status == 'Rejected':
                        return render(request, 'rejected_alert.html')
                    else:
                        return HttpResponseForbidden("Invalid login credentials or user not authorized.")
                else:
                    return HttpResponseForbidden("Invalid login credentials or user not authorized.")
            elif user.is_superuser:
                login(request, user)
                return redirect('siteusers:admin_home')
            else:
                return HttpResponseForbidden("Invalid login credentials or user not authorized.")
        else:
            return HttpResponseForbidden("Invalid login credentials.")
    else:
        return render(request, 'login.html')



def signup(request):
    return render(request,'signup.html')

@login_required
def house_resident(request):
    services = Service_Category.objects.all()
    return render(request,'houseresident_home.html',{'services':services})


def Explore_Service(request, pid):
    if not request.user.is_authenticated:
        return redirect('siteusers:Login_User')

    user = ""
    error = ""

    # Check if the request user has a valid ID
    if request.user.id:
        try:
            user = CustomUser.objects.get(id=request.user.id)
            try:
                # Try to get a HouseResident
                resident = House_Resident.objects.get(user=user)
                error = "pat"
            except House_Resident.DoesNotExist:
                try:
                    # Try to get a FlatResident if HouseResident doesn't exist
                    resident = Flat_Resident.objects.get(user=user)
                    error = "pat"  # You can modify this accordingly
                except Flat_Resident.DoesNotExist:
                    pass
        except User.DoesNotExist:
            pass

    # Assuming Service_Category and Status models are defined correctly
    ser = get_object_or_404(Service_Category, id=pid)
    sta, _ = Status.objects.get_or_create(status="Approve")
    order = Housemaid.objects.filter(service_name__category=ser.category, status=sta)


    d = {'error': error, 'ser': ser, 'order': order}

    return render(request, 'explore.html', d)

@login_required
def flat_resident(request):
    services = Service_Category.objects.all()
    return render(request,'flatresident_home.html',{'services':services})
@login_required
def housemaid_home(request):
    return render(request,'housemaid_home.html')


from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required
def admin_home(request):
    count = 0
    notfy = Notification.objects.filter(is_read=False)
    if notfy:
     count = notfy.count()
    return render(request, 'admin_home.html',{'count':count})

@login_required
def all_housemaid(request):
    housemaids = Housemaid.objects.all()
    return render(request, 'all_housemaid.html', {'housemaids': housemaids})

@login_required
def housemaid_detail(request, housemaid_id):
    pro = Housemaid.objects.get(id=housemaid_id)
    return render(request,'housemaid_detail.html',{'pro':pro})

@login_required
# def all_users(request):
#     house = House_Resident.objects.all()
#     flat = Flat_Resident.objects.all()
#
#
#     return render(request,'all_users.html',{'house':house,'flat':flat})


@login_required
def Change_status(request, pid):
    error = False
    pro1 = Housemaid.objects.get(id=pid)
    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        pro1.status = sta
        pro1.save()
        error = True
    d = {'pro': pro1, 'error': error}
    return render(request, 'status.html', d)

@login_required
def admin_update_status(request, housemaid_id):

    if request.method == 'POST':
        housemaid = get_object_or_404(Housemaid, id=housemaid_id)
        new_status = request.POST.get('status')

        if new_status == 'Approve':
            user_status = Status.objects.get(status=new_status)
            housemaid.status = user_status
        elif new_status == 'Rejected':
            user_status = Status.objects.get(status=new_status)
            housemaid.status = user_status

        housemaid.save()

    return redirect('siteusers:all_housemaid')

def houseresident_registration(request):
    if request.method == 'POST':
        # Extracting data from the POST request
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['pwd']

        contact = request.POST['contact']
        address = request.POST['address']
        image = request.FILES['image']

        user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.is_houseresident = True
        user.save()

        house_resident = House_Resident.objects.create(user=user, contact=contact, address=address, image=image)

        subject = 'Registration Confirmation'
        message = "Thankyou for registering"
        from_email = 'febathampi0@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, "Registered Successfully")
        return redirect('siteusers:Login_User')

    return render(request,'houseresident_registration.html')


def flatresident_registration(request):
    if request.method == 'POST':
        # Extracting data from the POST request
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password1 = request.POST['pwd']

        contact = request.POST['contact']
        address = request.POST['address']
        image = request.FILES['image']
        flat_name = request.POST['flat_name']
        caretaker_email = request.POST['caretaker_email']


        user = CustomUser.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
        user.is_flatresident = True
        user.save()
        # Creating a Flat_Resident profile for the user
        flat_resident = Flat_Resident.objects.create(user=user, contact=contact, address=address, image=image, flat_name=flat_name,caretaker_email=caretaker_email)
        subject = 'Registration Confirmation'
        message = "Thankyou for registering to the housemaid site."
        from_email = 'febathampi0@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, "Registered Successfully")

        return redirect('siteusers:Login_User')  # Redirect to the home page after registration

    return render(request, 'flatresident_registration.html')


def housemaid_registration(request):
    service_categories = Service_Category.objects.all()
    if request.method == 'POST':
        # User Information
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['pwd']

        # Housemaid Information
        contact = request.POST['contact']
        address = request.POST['address']
        doj = datetime.date.today()
        dob = request.POST['dob']
        id_type = request.POST['id_type']
        service_name = request.POST['service_name']
        experience = request.POST['experience']
        id_card = request.FILES['id_card']
        image = request.FILES['image']
        rate_per_hour = request.POST['rate_per_hour']
        # Creating User
        user =CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        user.is_housemaid = True
        user.save()
        # Fetching or creating Status and City instances
        status, created = Status.objects.get_or_create(status='pending')


        # Creating a Housemaid profile for the user
        housemaid = Housemaid.objects.create(
            status=status,

            user=user,
            contact=contact,
            address=address,
            doj=doj,
            dob=dob,
            id_type=id_type,
            service_name=Service_Category.objects.get(category=service_name),  # Assuming Service_Category has a 'name' field
            experience=experience,
            id_card=id_card,
            image=image,
            rate_per_hour = rate_per_hour
        )
        subject = 'Registration Confirmation'
        message = "Thankyou for registering to the housemaid site."
        from_email = 'febathampi0@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        messages.success(request, "Registered Successfully")
        return redirect('siteusers:Login_User')

    return render(request,'housemaid_registration.html',{'service_categories': service_categories})
@login_required
def view_service(request):
    ser = Service_Category.objects.all()
    d = {'ser':ser}
    return render(request,'view_service.html',d)

@login_required
def edit_service(request,pid):

    error=False
    ser = Service_Category.objects.get(id=pid)
    if request.method == "POST":
        n = request.POST['cat']
        try:
            i = request.FILES['image']
            ser.image = i
            ser.save()
        except:
            pass
        de = request.POST['desc']
        ser.category = n
        ser.desc = de
        ser.save()
        error=True
    d = {'error':error,'ser':ser}
    return render(request,'edit_service.html',d)
@login_required
def delete_service(request,pid):
    ser = Service_Category.objects.get(id=pid)
    ser.delete()
    return redirect('siteusers:view_service')
@login_required
def add_service(request):

    error=False
    if request.method == "POST":
        n = request.POST['cat']
        i = request.FILES['image']
        de = request.POST['desc']
        Service_Category.objects.create(category=n,image=i,desc=de)
        error=True
    d = {'error':error}
    return render(request,'add_service.html',d)

def all_user(request):

    ser = Customer.objects.all()
    d = {'ser':ser}
    return render(request,'all_user.html',d)

def all_service_man(request):

    ser = Housemaid.objects.all()
    d = {'ser':ser}
    return render(request,'all_service_man.html',d)

def new_service_man(request):
    status = Status.objects.get(status="pending")
    ser = Housemaid.objects.filter(status=status)
    d = {'ser':ser}
    return render(request,'new_service_man.html',d)

def all_houseusers(request):

    ser = House_Resident.objects.all()
    d = {'ser':ser}
    return render(request,'all_houseusers.html',d)
def delete_houseuser(request,pid):
    ser = House_Resident.objects.get(id=pid)
    ser.delete()
    return redirect('siteusers:all_houseusers')
def all_flatusers(request):

    ser = Flat_Resident.objects.all()
    d = {'ser':ser}
    return render(request,'all_flatusers.html',d)
def delete_flatuser(request,pid):
    ser = Flat_Resident.objects.get(id=pid)
    ser.delete()
    return redirect('siteusers:all_flatusers')

def delete_service_man(request,pid):
    ser = Housemaid.objects.get(id=pid)
    ser.delete()
    return redirect('siteusers:all_service_man')

def delete_admin_order(request,pid):
    ser = Order.objects.get(id=pid)
    ser.delete()
    return redirect('siteusers:Admin_Order')
def all_users(request):
    flat_users = Flat_Resident.objects.all()
    house_users = House_Resident.objects.all()
    all_users = list(flat_users) + list(house_users)
    context = {
        'users': all_users
    }
    return render(request, 'all_users.html', context)
def calculate_payment_amount(days,hours, rate_per_hour):
    return Decimal(days)*Decimal(hours) * rate_per_hour
@login_required
def housecustomer_booking(request, pid):
    if not request.user.is_authenticated:
        return redirect('siteusers:Login_User')

    user = request.user
    print(user)
    error = ""
    try:
        sign = House_Resident.objects.get(user=user)

        error = "pat"
    except House_Resident.DoesNotExist:
        # Handle the case when the user is not a house resident
        return HttpResponseBadRequest("Invalid user type")

    terror = False

    try:
        ser1 = Housemaid.objects.get(id=pid)
        print(ser1)
    except Housemaid.DoesNotExist:
        # Handle the case when the specified housemaid does not exist
        return HttpResponseBadRequest("Invalid housemaid ID")

    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        add = request.POST['add']
        dat = request.POST['date']
        da = request.POST['day']
        ho = request.POST['hour']

        # Fetch the housemaid's rate per hour
        rate_per_hour = ser1.rate_per_hour
        print(rate_per_hour)
        service_category = ser1.service_name
        print(service_category)

        # Convert days (da) and hours (ho) to Decimal before passing them to calculate_payment_amount
        days = Decimal(da)
        hours = Decimal(ho)

        # Check if rate_per_hour is not None before calculating payment amount
        if rate_per_hour is not None:
            payment_amount = calculate_payment_amount(days, hours, rate_per_hour)
        else:
            # Handle the case when rate_per_hour is None
            payment_amount = Decimal(0)  # or any default value you prefer

        print(payment_amount)

        # Create order
        st = Status.objects.get(status="pending")
        wk = Work.objects.get(work="pending")
        pd = Paid.objects.get(paid="pending")
        order = Order.objects.create(
            status=st,
            work_completed=wk,
            paid=pd,
            service=ser1,  # Assuming Housemaid has a service_name field
            customer=sign,
            book_date=dat,
            book_days=da,
            book_hours=ho,
            payment_amount=payment_amount
        )

        return redirect('siteusers:Customer_Order')

    d = {'error': error, 'ser': sign, 'terror': terror}
    return render(request, 'bookinghouse.html', d)
@login_required
def Customer_Order(request):
    user= CustomUser.objects.get(id=request.user.id)
    error=""
    try:
        sign = House_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
        pass
    order = Order.objects.filter(customer=sign)
    d = {'error':error,'order':order}
    return render(request,'customer_order.html',d)

@login_required
def admin_update_status(request, order_id):

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('work')

        if new_status == 'pending':
            work_status = Work.objects.get(work=new_status)
            order.work_completed = work_status
        elif new_status == 'completed':
            work_status = Work.objects.get(work=new_status)
            order.work_completed = work_status

        order.save()

    return redirect('siteusers:Customer_Order')
def admin_update_status_2(request, order_id):

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('paid')

        if new_status == 'pending':
            paid_status = Paid.objects.get(paid=new_status)
            order.paid = paid_status
        elif new_status == 'paid':
            paid_status = Paid.objects.get(paid=new_status)
            order.paid = paid_status

        order.save()

    return redirect('siteusers:Customer_Order')


def send_approval_notification(order, request):
    subject = 'New Booking Approval Required'
    caretaker_email = order.flat_resident.caretaker_email
    print(caretaker_email)
    # Generate the approval link using reverse and request.build_absolute_uri
    approval_link = request.build_absolute_uri(reverse('siteusers:approval_of_caretaker', args=[order.id]))

    # Render the email template
    context = {'order': order,'approval_link':approval_link}
    message = render_to_string('booking_approval_email_template.html', context)

    # Send the email
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [caretaker_email])

def approval_of_caretaker(request, order_id):

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        print(order)
        new_status = request.POST.get('caretaker_approval')

        if new_status == 'Approve':
            paid_status = CaretakerApproval.objects.get(caretaker_approval=new_status)
            order.caretaker_approval = paid_status
        elif new_status == 'Rejected':
            paid_status = CaretakerApproval.objects.get(caretaker_approval=new_status)
            order.caretaker_approval = paid_status

        order.save()


        return redirect('siteusers:home')
    context = {
        'order_id': order_id

    }
    return render(request,'approve_caretaker.html',context)


@login_required
def flat_resident_booking(request, pid):
    if not request.user.is_authenticated:
        return redirect('siteusers:Login_User')

    user = request.user
    error = ""

    try:
        flat_resident = Flat_Resident.objects.get(user=user)
    except Flat_Resident.DoesNotExist:
        return HttpResponseBadRequest("Invalid user type")

    try:
        housemaid = Housemaid.objects.get(id=pid)
    except Housemaid.DoesNotExist:
        return HttpResponseBadRequest("Invalid housemaid ID")

    if request.method == "POST":
        n = request.POST['name']
        c = request.POST['contact']
        add = request.POST['add']
        dat = request.POST['date']
        da = request.POST['day']
        ho = request.POST['hour']

        # Fetch the housemaid's rate per hour
        rate_per_hour = housemaid.rate_per_hour
        print(rate_per_hour)
        service_category = housemaid.service_name
        print(service_category)
        payment_amount = calculate_payment_amount(da, ho, housemaid.rate_per_hour)
        st = Status.objects.get(status="pending")
        wk = Work.objects.get(work="pending")
        pd = Paid.objects.get(paid="pending")
        bc = CaretakerApproval.objects.get( caretaker_approval="pending")
        order = Order.objects.create(
            status=st,
            work_completed=wk,
            paid=pd,
            service=housemaid,
            flat_resident=flat_resident,
            book_date=dat,
            book_days=da,
            book_hours=ho,
            payment_amount=payment_amount,
            caretaker_approval=bc  # Set initial approval status to False
        )

        # Check if the booking is made by a flat resident
        if flat_resident:
            send_approval_notification(order, request)
            # Send email notification to caretaker with approval link


        return redirect('siteusers:Customer_Order1')

    context = {'error': error, 'ser': flat_resident, 'terror': False}
    return render(request, 'booking1.html', context)
def admin_update_status1(request, order_id):

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('work')

        if new_status == 'pending':
            work_status = Work.objects.get(work=new_status)
            order.work_completed = work_status
        elif new_status == 'completed':
            work_status = Work.objects.get(work=new_status)
            order.work_completed = work_status

        order.save()

    return redirect('siteusers:Customer_Order1')



@login_required
def Customer_Order1(request):
    user= CustomUser.objects.get(id=request.user.id)
    error=""
    try:
        sign = Flat_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
        pass
    order = Order.objects.filter(flat_resident=sign)
    d = {'error':error,'order':order}
    return render(request,'customer_order1.html',d)



def admin_update_status_21(request, order_id):

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('paid')

        if new_status == 'pending':
            paid_status = Paid.objects.get(paid=new_status)
            order.paid = paid_status
        elif new_status == 'paid':
            paid_status = Paid.objects.get(paid=new_status)
            order.paid = paid_status

        order.save()

    return redirect('siteusers:Customer_Order1')

import razorpay
@login_required
def payment_page(request, order_id):
        order = Order.objects.get(id=order_id)
        if request.method == 'POST':
            # Handle payment logic here using the provided payment details
            cardholder_name = request.POST.get('cardholder_name')
            card_number = request.POST.get('card_number')
            expiration_date = request.POST.get('expiration_date')
            cvv = request.POST.get('cvv')
            amount_received=request.POST.get('amount_received')
            # Create payment associated with the order
            payment = Payment.objects.create(
                cardholder_name=cardholder_name,
                amount_received=amount_received,

            )

            # Associate the payment with the order
            order.payment = payment
            order.save()


            messages.success(request, 'Payment done successfully!')
            return redirect('siteusers:home')  # You can redirect or render a success page here

        context = {'order': order}
        return render(request, 'payment.html', context)

def contact(request):
    context={}
    if request.method=="POST":
        name = request.POST.get('name','')
        email = request.POST.get('email', '')
        phone = request.POST.get('Phone', '')
        message = request.POST.get('message', '')
        status = Status.objects.get(status="unread")
        contact=Contact(name=name,email=email,phone=phone,message=message,status=status)
        contact.save()
        context['message']=f"Dear {name},thanks for your time,will get back to you soon."
    return render(request, 'contact.html',context)



def user_logout(request):
    logout(request)
    return home(request)

@login_required
def admin_home(request):
    count = 0
    notfy = Notification.objects.filter(is_read=False)
    if notfy:
     count = notfy.count()
    return render(request, 'admin_home.html',{'count':count})

@login_required
def Admin_Order(request):
    order = Order.objects.all()
    seen_notifies = Notification.objects.filter(is_read=False)

    for notify in seen_notifies:
        notify.is_read = True
        notify.save()

    d = {'order': order}
    return render(request, 'all_orderss.html', d)


@login_required
def Order_detail(request,pid):

    pro1 = Order.objects.get(id=pid)
    d = {'pro':pro1}
    return render(request,'order_detail.html',d)

@login_required
def Order_status(request, pid):
    error = False
    pro1 = Order.objects.get(id=pid)

    if request.method == "POST":
        stat = request.POST['stat']
        sta = Status.objects.get(status=stat)
        previous_status = pro1.status  # Save the previous status for comparison

        pro1.status = sta
        pro1.save()
        login_url = request.build_absolute_uri(reverse('siteusers:Login_User'))
        # Check if the status is updated to 'approve'
        if pro1.status.status == 'Approve' and previous_status != 'Approve':
            # Fetch the housemaid associated with the order
            housemaid = pro1.service
            print(housemaid)# Assuming 'service' is the ForeignKey to the Housemaid model
            if housemaid:
                # Send an email to the housemaid
                subject = 'new booking'
                message = f"You have a new booking. Please log in to the site for more information.\n\nLogin here: {login_url}"
                from_email = 'febathampi0@gmail.com'
                to_email = housemaid.user.email
                print(to_email)

                send_mail(subject, message, from_email, [to_email])

        error = True

    d = {'pro': pro1, 'error': error}
    return render(request, 'order_status.html', d)

from django.shortcuts import render
from .models import Housemaid, Order


@login_required
def housemaid_bookings(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        try:
            # Get the current housemaid (assuming the logged-in user is a housemaid)
            housemaid = Housemaid.objects.get(user=request.user)

            # Fetch all bookings related to the housemaid
            bookings = Order.objects.filter(service=housemaid,status__status='Approve')

            context = {'bookings': bookings}
            return render(request, 'housemaid_bookings.html', context)
        except Housemaid.DoesNotExist:
            # Handle the case when the user is not a housemaid
            return render(request, 'housemaid_bookings.html', {'error': 'You are not a housemaid.'})
    else:
        # Redirect to the login page or show an error message
        return render(request, 'housemaid_bookings.html', {'error': 'You need to log in to view bookings.'})


def services(request):
    return render(request, 'services.html')


@login_required
def house_resident_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    error = ""
    try:
        sign = House_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'houseresident_profile.html',d)

@login_required
def flat_resident_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Flat_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'flatresident_profile.html',d)


@login_required
def housemaid_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    error = ""
    try:
        sign = House_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
    terror = False
    d = {'pro':sign,'error':error}
    return render(request,'housemaid_profile.html',d)


@login_required
def edit_house_resident_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    error = ""
    try:
        sign = House_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        sign.address = ad
        sign.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.save()
        terror = True
    d = {'terror':terror,'error':error,'pro':sign,'ser':ser}
    return render(request, 'edit_house_resident_profile.html',d)


@login_required
def edit_flat_resident_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Flat_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        sign.address = ad
        sign.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        user.save()
        sign.save()
        terror = True
    d = {'terror':terror,'error':error,'pro':sign,'ser':ser}
    return render(request, 'edit_flat_resident_profile.html',d)


@login_required
def edit_housemaid_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    error = ""
    try:
        sign = House_Resident.objects.get(user=user)
        error = "pat"
    except:
        sign = Housemaid.objects.get(user=user)
    terror = False
    ser = Service_Category.objects.all()
    car = ID_Card.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        try:
            i = request.FILES['image']
            sign.image=i
            sign.save()
        except:
            pass
        try:
            i1 = request.FILES['image1']
            sign.id_card=i1
            sign.save()
        except:
            pass
        ad = request.POST['address']
        e = request.POST['email']
        con = request.POST['contact']
        # se = request.POST['service']
        card = request.POST['card']
        ex = request.POST['exp']
        dob = request.POST['dob']
        if dob:
            sign.dob=dob
            sign.save()
        sign.address = ad
        sign.contact=con
        user.first_name = f
        user.last_name = l
        user.email = e
        sign.id_type = card
        sign.experience = ex
        # sign.service_name = se
        user.save()
        sign.save()
        terror = True
    d = {'terror':terror,'error':error,'pro':sign,'car':car,'ser':ser}
    return render(request, 'edit_housemaid_profile.html',d)

def about(request):
    return render(request, 'about.html')


def new_message(request):
    sta = Status.objects.get(status='unread')
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser': pro1}
    return render(request, 'new_message.html', d)


def read_message(request):
    sta = Status.objects.get(status='read')
    pro1 = Contact.objects.filter(status=sta)
    d = {'ser': pro1}
    return render(request, 'read_message.html', d)
def confirm_message(request,pid):
    ser = Contact.objects.get(id=pid)
    sta = Status.objects.get(status='read')
    ser.status = sta
    ser.save()
    return redirect('siteusers:new_message')


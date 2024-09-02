import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .forms import RegistrationForm, OTPForm, LoginForm, ServiceForm, SubscriptionForm
from .models import Service, Subscription

import razorpay

otp_storage = {}

def send_otp(email):
    otp = str(random.randint(100000, 999999))
    send_mail(
        'Your OTP Code',
        f'Your OTP code to register into the app is {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    otp_storage[email] = otp

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            send_otp(user.email)
            request.session['email'] = user.email
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        email = request.session.get('email')
        if form.is_valid():
            otp = form.cleaned_data['otp']
            if otp_storage.get(email) == otp:
                user = User.objects.get(email=email)
                login(request, user)
                del otp_storage[email]
                return redirect('home')
            else:
                form.add_error(None, "Invalid OTP")
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})

@login_required
def home(request):
    services = Service.objects.filter(active=True)
    return render(request, 'home.html', {'services': services})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('service_list')
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form})

def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    return render(request, 'service_detail.html', {'service': service})

@login_required
def update_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('service_detail', pk=service.pk)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'update_service.html', {'form': form})

@login_required
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('service_list')
    return render(request, 'delete_service.html', {'service': service})

def service_list(request):
    services = Service.objects.all()
    return render(request, 'service_list.html', {'services': services})

# Razorpay client setup
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def subscribe(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            amount = int(service.service_price * 100)  # amount in paise
            # Create a Razorpay order
            razorpay_order = client.order.create(dict(amount=amount, currency='INR', payment_capture='1'))
            subscription = Subscription.objects.create(
                service=service,
                address=address,
                amount=amount / 100,  # amount in rupees
                payment_id=razorpay_order['id'],
                payment_status='Pending'
            )
            return render(request, 'payment.html', {'order_id': razorpay_order['id'], 'amount': amount, 'key_id': settings.RAZORPAY_KEY_ID})
    else:
        form = SubscriptionForm()

    net_price = service.service_price + service.service_tax
    return render(request, 'subscribe.html', {'form': form, 'service': service, 'net_price': net_price})

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        subscription_id = request.POST.get('subscription_id')
        signature = request.POST.get('razorpay_signature')

        # Verify payment signature
        try:
            client.utility.verify_payment_signature(dict(payment_id=payment_id, order_id=subscription_id, signature=signature))
            subscription = get_object_or_404(Subscription, payment_id=subscription_id)
            subscription.payment_status = 'Completed'
            subscription.save()
            return redirect('thank_you')  # Redirect to thank you page
        except Exception as e:
            # Handle verification failure
            subscription = get_object_or_404(Subscription, payment_id=subscription_id)
            subscription.payment_status = 'Failed'
            subscription.save()
            return redirect('payment_failed')  # Redirect to failure page

def thank_you(request):
    return render(request, 'thank_you.html')

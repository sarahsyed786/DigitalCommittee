
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from requests import request
from django.shortcuts import render, redirect
from .forms import EnrollmentForm
from .models import Enrollment, Package,UserProfile,ResultHistory
from django.contrib.auth.forms import UserCreationForm
from project import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta
from django.core.cache import cache
from .forms import InterestForm
import random
from time import sleep
from django.contrib.auth.decorators import user_passes_test
# Create your views here.


def home(request):
    return render(request, "fair_collection/index.html" )

def signup(request):
    if request.method ==    'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        address = request.POST['address']
        email = request.POST['email']
        password = request.POST['password']
        cpass = request.POST['cpass']

        # Validations
        if User.objects.filter(username=username):
            messages.error(request, 'User name already exist! Please try some other user name. ')
            return redirect('/signup')
        
        if User.objects.filter(email=email):
            messages.error(request,'Email already registered!')
            return redirect('/signup')
        
        if len(username)>10:
            messages.error(request,'Username must be under 10 characters.')
            return redirect('/signup')

        if len(username)<5:
            messages.error(request,' Username must have atleast 5 characters ')
            return redirect('/signup')
        
        if password!=cpass:
            messages.error(request,"Password didn't match!")
            return redirect('/signup')
        
        if not username.isalnum():
            messages.error(request,'Username must contain alphabats and numbers and no special charachers in it')
            return redirect('/signup')


        myuser = User.objects.create_user(username, email, password) #Create user 
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.address1 = address

        myuser.save() #save users data
        messages.success(request, "Your Account has been successfully created.")

        return redirect('/signin') 


    return render(request, "fair_collection/signup.html" )

def signin(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.username
            return render(request, "fair_collection/front.html", {'fname':fname} )

        else:
            messages.error(request, "Bad Credential")
            return redirect("home")

    return render(request, "fair_collection/signin.html" )




def package_list(request):
    packages = Package.objects.all()
    return render(request, 'fair_collection/package_list.html', {'packages': packages})

def express_interest(request):
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save(commit=False)
            interest.user = request.user
            interest.save()

            # Send email notification to the admin
            send_interest_notification(interest)

            return redirect('package_list')  # Redirect to package list or another page
    else:
        form = InterestForm()

    return render(request, 'fair_collection/express_interest.html', {'form': form})

def send_interest_notification(interest):
    subject = f"New Interest: {interest.package_name}"
    message = render_to_string('fair_collection/interest_notification_email.html', {'interest': interest})
    plain_message = strip_tags(message)
    from_email = [User.email] # Update with your email
    to_email = settings.EMAIL_HOST_USER    # Update with admin's email
    send_mail(subject, plain_message, from_email, [to_email], html_message=message)



def enroll_package(request, package_id):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = request.user
            enrollment.package_id = package_id
            enrollment.save()
            return redirect('package_list')
    else:
        form = EnrollmentForm()

    return render(request, 'fair_collection/enroll_package.html', {'form': form})


def user_dashboard(request):
    if User is authenticate:
        User.save()
    return render(request, 'fair_collection/user_dashboard.html' )


# def generate_result(request):
#     # last_announcement_timestamp = cache.get('last_announcement_timestamp')

#     # if last_announcement_timestamp:
#         # Calculate the time difference since the last announcement
#         # time_difference = datetime.now() - last_announcement_timestamp

#         # If less than 30 days have passed, disable the button
#         # if time_difference < timedelta(days=30):
#         #     return render(request, 'fair_collection/generate_result_disabled.html')

#     # If the button is not disabled or 30 days have passed, proceed with generating a result
#     random_user = User.objects.order_by('?').first()

#     # Update the last announcement timestamp
#     # cache.set('last_announcement_timestamp', datetime.now(), 30 * 24 * 60 * 60)  # Cache for 30 days

#     return render(request, 'fair_collection/generate_result.html', {'random_user': random_user})

def generate_result(request):
    sleep(3)
    try:
        # Get the package of the user generating the result
        user_profile = UserProfile.objects.get(user=request.user)
        user_package = user_profile.package

        # Get all users with the same package
        users_with_same_package = UserProfile.objects.filter(package=user_package)

        # Check if the form is submitted
        if request.method == 'POST':
            # Move the previous random user to the result history
            result_history = ResultHistory(user=user_profile.user, result='some_result')
            result_history.save()

            # Get a new random user
            new_random_user = get_random_user(users_with_same_package)

            # Render the template with the new random user and users with the same package
            return render(request, 'fair_collection/generate_result.html', {'random_user': new_random_user, 'users_with_same_package': users_with_same_package})

        # Render the template without an initial result
        return render(request, 'fair_collection/generate_result.html', {'users_with_same_package': users_with_same_package})

    except UserProfile.DoesNotExist:
        # Handle the case when UserProfile does not exist for the current user
        return render(request, 'fair_collection/generate_result.html', {'error_message': 'UserProfile does not exist for the current user.'})
    
    


def get_random_user(queryset):
    return queryset.order_by('?').first()


def signout(request):
   logout(request)
   messages.success(request, "Logged Out Successfully!")
   return redirect("home")

def features(request):   
        return render(request, "fair_collection/features.html" )

def front(request):
        return render(request, "fair_collection/front.html" )

def result_history(request):
    history = ResultHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "fair_collection/result_history.html", {'history': history} )

def paynow(request):  
        return render(request, "fair_collection/pay.html" )

def about(request):
    return render(request, "fair_collection/about.html" )


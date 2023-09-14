from django.shortcuts import render,redirect
from django.urls import path,include
from django.shortcuts import HttpResponse
from courses.models import Course
from django.contrib.auth import logout,login
# from django.contrib.auth.models import User
from courses.models import User
from django.contrib.auth import login, authenticate
from courses.forms import UserRegistrationForm,UserLoginForm
from django.views import View
from django.views.generic.edit import FormView
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import messages

from django.core.mail import send_mail
from django.core.exceptions import ValidationError

from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from courses.helpers import send_forget_password_mail

import random
import smtplib


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            role = form.cleaned_data.get("role")
            request.session["username"] = username
            request.session["role"] = role
            user = form.save()
            return redirect('login')
        else:
            errors = form.errors
    else:
        form = UserRegistrationForm()
    errors = None
    return render(request, "courses/signup.html", {"form": form, "errors": errors})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from courses.models import User
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from courses.serializers import UserSerializer, LoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({'access_token': access_token, 'refresh_token': refresh_token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    errors = {}
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            role = form.cleaned_data.get("role")
            try:
                username = User.objects.get(email=email, role=role).username
            except:
                try:
                    username = User.objects.get(email=email)
                    errors["invalid_role"] = "Selected role not associated with this email"
                    return render(request, "courses/login.html", {"form": form, "errors": errors})
                except User.DoesNotExist:
                    errors["bad_credentials"] = "Invalid Email / Password"
                    return render(request, "courses/login.html", {"form": form, "errors": errors})
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.role == role:
                    request.session["username"] = username
                    request.session["role"] = role
                    email = form.cleaned_data['email']
                    otp = ''.join(random.choices('0123456789', k=6))
                    request.session['otp'] = otp
                    send_mail(
                        'OTP Verification',
                        f'Your OTP is: {otp}',
                        'swaroopbhat12345@gmail.com',
                        [email],
                        fail_silently=False,
                    )
                    login(request, user)  
                    return redirect('otp-verification')
                else:
                    errors["invalid_role"] = "Selected role not associated with this email"
                    return render(request, "courses/login.html", {"form": form, "errors": errors})
            else:
                errors["bad_credentials"] = "Invalid Email / Password"
                return render(request, "courses/login.html", {"form": form, "errors": errors})
        else:
            errors["invalid_data"] = "Invalid form data. Please try again."
            return render(request, "courses/login.html", {"form": form, "errors": errors})
    else:
        form = UserLoginForm()
        errors = {}
    return render(request, "courses/login.html", {"form": form, "errors": errors})


def otp_verification_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == request.session.get('otp'):
            role = request.session.get('role')
            if role == 'student':
                return redirect('home')  
            elif role == 'teacher':
                return redirect('display_course_details')   
        else:
            errors = {'invalid_otp': 'Invalid OTP. Please try again.'}
            return render(request, 'courses/otp_verification.html', {'errors': errors})
    return render(request, 'courses/otp_verification.html')


def signout(request):
    logout(request)
    return redirect('home')

def teacher_signout(request):
    logout(request)
    return redirect('login')



            

   
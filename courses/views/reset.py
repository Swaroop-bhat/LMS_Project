from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from courses.models import User
import hashlib


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            token = get_random_string(length=40)
            user.reset_token = token
            user.save()
            reset_link = request.build_absolute_uri(f'/reset-password/{token}/')
            send_reset_email(email, reset_link)
            messages.success(request, 'Password reset link sent to your email.')
        except User.DoesNotExist:
            messages.error(request, 'Email not found.')
    return render(request, 'courses/forgot_password.html')


def reset_password_view(request, token):
    try:
        user = User.objects.get(reset_token=token)
        if request.method == 'POST':
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']  
            if len(new_password) >= 8:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    user.reset_token = None
                    user.save()
                    messages.success(request, 'Password reset successful.')
                    return redirect('login')
                else:
                    messages.error(request, 'Passwords do not match.')
            else:
                messages.error(request, 'Password must be at least 8 characters long.')
    except User.DoesNotExist:
        messages.error(request, 'Invalid token.')
    return render(request, 'courses/reset_password.html', {'token': token})


def send_reset_email(email, reset_link):
    subject = 'Password Reset'
    message = f'Click the following link to reset your password: {reset_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

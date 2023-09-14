from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate,login,get_user_model
from django.core.mail import send_mail
import random
from django.views.generic.edit import FormView






#main-earlier
# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(max_length=200, required=True, label='Email address')

#     def clean(self):
#         cleaned_data = super().clean()

#         email = cleaned_data.get('username')  # Use 'username' instead of 'email'

#         if email:
#             try:
#                 user = User.objects.get(email=email)  
#             except User.DoesNotExist:
#                 raise forms.ValidationError("This email is not registered.")

#         return cleaned_data


from django import forms

class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        widget=forms.Select,
        initial="student",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["class"] = "login_username"
        self.fields["email"].widget.attrs["placeholder"] = " "
        self.fields["password"].widget.attrs["class"] = "login_password"
        self.fields["password"].widget.attrs["placeholder"] = " "
        self.fields["role"].widget.attrs["class"] = "login_role"
        self.fields["role"].widget.attrs["placeholder"] = " "



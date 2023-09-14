from django.contrib.auth.forms import UserCreationForm
from django import forms
from courses.models import User
class UserRegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select, initial="student")
    email = forms.EmailField(max_length=255, label="Email")
    username = forms.CharField(max_length=50, label="Username")

    class Meta:
        model = User
        fields = ["email", "username", "role"]

    def clean(self):    
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        role = cleaned_data.get("role")
        if User.objects.filter(email=email, role__in=["student", "teacher"]).exists():
            existing_roles = User.objects.filter(email=email).values_list(
                "role", flat=True)

            if "student" in existing_roles and role == "student":
                raise forms.ValidationError("This email is already registered as a student.")

            if "teacher" in existing_roles and role == "teacher":
                raise forms.ValidationError("This email is already registered as a teacher.")   
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["placeholder"] = " "
        self.fields["username"].widget.attrs["placeholder"] = " "
        self.fields["password1"].widget.attrs["placeholder"] = " "
        self.fields["password2"].widget.attrs["placeholder"] = " "
        self.fields["role"].widget.attrs["placeholder"] = " "

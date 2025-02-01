from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserRegister
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):


    class Meta:
        model = UserRegister
        fields = ["businessname","username", "phone" ,"email", "password1", "password2"]
        labels = {
            'businessname': 'Business Name',
            
        }
        help_texts = {
            
            'username': '',
            'password1': '',
            'password2': '',
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

 

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn’t match.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
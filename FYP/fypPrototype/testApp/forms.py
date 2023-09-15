from django import forms
from django.forms import ModelForm, ImageField
from .models import *
from django.contrib.auth.models import User
#To authenticate users:
from django.contrib.auth import authenticate, login, logout

class LoginForm(forms.Form):
    username=forms.CharField(max_length=65)
    password=forms.CharField(max_length=65, widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError({"password":"Invalid username or password", "username":""})
        return self.cleaned_data
    
    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        help_texts = {
            'username': None,
        }
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError({
                "confirm_password":"Password and Confirm password does not match"
            })

class SignUpExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise_Day
        fields = ()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('name',)

class SettingUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class ExerciseDayForm(forms.ModelForm):
    class Meta:
        model =  Exercise_Day
        fields = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')
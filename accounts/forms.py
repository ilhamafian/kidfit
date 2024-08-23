from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import CustomUser
from .models import ChildInfo


class OrderForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class ChildInfoForm(forms.ModelForm):
    class Meta:
        model = ChildInfo
        exclude = ['user']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

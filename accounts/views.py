from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import OrderForm, CreateUserForm


def home(request):
    return render(request, 'accounts/login.html')


def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

from .models import ChildInfo

# Create your views here.
from .forms import OrderForm, CreateUserForm


def home(request):
    return render(request, 'accounts/login.html')


# There seems to be something wrong with the login page, even if I entered the right password it will still show 'Error Loggin In' in the
# admin view. Plus, why does it even appear in the admin view? And it does not redirect back to the homepage. Solve it, check if the
# architecture is correct, it's not MVC, it's Model-Template-View if you're in Django.

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You\'re logged in'))
            return redirect('/home')
        else:
            messages.info(request, ('Username or Email is incorrect'))
            # context = {'error_message': 'Invalid Login Credentials '}

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Welcome to KidFit, ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def childInfo(request):
    if request.method == 'POST':
        childs_name = request.POST['childs_name']
        gender = request.POST['gender']
        measurement = request.POST['measurement']
        weight = request.POST['weight']
        height = request.POST['height']
        inseam = request.POST['inseam']
        chest = request.POST['chest']
        waist = request.POST['waist']
        hip = request.POST['hip']
        foot = request.POST['foot']

        new_child = ChildInfo(childs_name=childs_name, gender=gender, metric=metric, weight=weight,
                              height=height, inseam=inseam, chest=chest, waist=waist, hip=hip, foot=foot)
        new_child.save()

    return render(request, '/child-info', {})

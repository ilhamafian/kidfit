from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import ChildInfo, SizeCharts

# Create your views here.
from .forms import OrderForm, CreateUserForm, ChildInfoForm


def home(request):
    return render(request, 'accounts/login.html')


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ('You\'re logged in'))
            return redirect('/both')
        else:
            messages.info(request, ('Username or Email is incorrect'))
            # context = {'error_message': 'Invalid Login Credentials '}

    context = {}
    return render(request, 'accounts/login.html', context)


def sizeChart(request):
    if request.method == "POST":
        searched = request.POST['searched']
        brands = SizeCharts.objects.filter(brand__contains=searched)
        return render(request, 'size-charts.html', {'searched': searched, 'brands': brands})
    else:

        return render(request, 'size-charts.html', {})


def displayChart(request, pk):
    chart = SizeCharts.objects.get(id=pk)
    return render(request, 'display-chart.html', {'chart': chart})


@login_required
def changePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            print('good its fucking working')
            return redirect('settings/')
        else:
            messages.error(request, 'Please correct the error below.')
            print('something wong')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'settings.html', {
        'form': form
    })


@login_required
def updateUserInfo(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')

        # Update the user's information
        request.user.username = new_username
        request.user.email = new_email
        request.user.save()

        messages.success(
            request, 'Your information has been successfully updated!')
        # Redirect to the user's profile or another page
        return redirect('settings/')

    return render(request, 'settings.html')


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


@login_required
def childInfo(request):
    form = ChildInfoForm()
    user_child_info = ChildInfo.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ChildInfoForm(request.POST)
        if form.is_valid():
            child_info = form.save(commit=False)
            child_info.user = request.user
            child_info.save()
            print('Form has been saved')
            return redirect('/child-info')
        else:
            print(form)

    return render(request, 'accounts/child-info.html', {'form': form, 'user_child_info': user_child_info})


@login_required
def childSave(request):
    form = ChildInfoForm()
    user_child_info = ChildInfo.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ChildInfoForm(request.POST)
        if form.is_valid():
            child_info = form.save(commit=False)
            child_info.user = request.user
            child_info.save()
            print('Form has been saved')
            return redirect('/child-info')
        else:
            print(form.errors)

    return render(request, 'topbottom-output.html', {'form': form, 'user_child_info': user_child_info})


@login_required
def delete(request, child_info_id):
    dele = ChildInfo.objects.get(pk=child_info_id)
    dele.delete()

    return redirect('/child-info')

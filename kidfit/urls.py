"""kidfit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import fuzzy
from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('home', TemplateView.as_view(template_name='base.html')),
    path('size-conversion', TemplateView.as_view(template_name='size-conversion.html')),
    path('size-charts', TemplateView.as_view(template_name='size-charts.html')),
    path('profile', TemplateView.as_view(template_name='profile.html')),
    path('child-info', TemplateView.as_view(template_name='child-info.html')),
    path('output', fuzzy.output),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('forgot-password/', TemplateView.as_view(template_name='forgot-password.html')),
    path("__debug__/", include("debug_toolbar.urls")),
]

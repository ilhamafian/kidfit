# from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    # path('account/', include('accounts.urls')),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('childInfo/', views.childInfo, name="childInfo"),
    path('childSave/', views.childSave, name="childSave"),
]

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
from django.conf import settings
from django.conf.urls.static import static
from accounts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('accounts.urls')),
    path('both/', TemplateView.as_view(template_name='topbottom.html')),
    path('top/', TemplateView.as_view(template_name='top.html')),
    path('bottom/', TemplateView.as_view(template_name='bottom.html')),
    path('', TemplateView.as_view(template_name='home.html')),
    path('size-conversion', TemplateView.as_view(template_name='size-conversion.html')),
    path('size-charts/', TemplateView.as_view(template_name='size-charts.html')),
    path('size-charts', views.sizeChart, name='sizeChart'),
    path('display-chart/', TemplateView.as_view(template_name="display-chart.html")),
    path('display-chart/<int:pk>', views.displayChart, name="displayChart"),
    path('profile', TemplateView.as_view(template_name='profile.html')),
    path('child-info', views.childInfo, name="childInfo"),
    path('delete-measurement/<child_info_id>',
         views.delete, name="delete-measurement"),
    path('output', fuzzy.output, name='output'),
    path('topbottom-output/',
         TemplateView.as_view(template_name='topbottom-output.html')),
    path('topbottom-output', views.childSave, name="childSave"),
    path('settings/', TemplateView.as_view(template_name='settings.html')),
    path('settings', views.updateUserInfo, name='updateUserInfo'),
    path('settings', views.changePassword, name='changePassword'),
    path('top-output/', TemplateView.as_view(template_name='top-output.html')),
    path('bottom-output/', TemplateView.as_view(template_name='bottom-output.html')),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('forgot-password/', TemplateView.as_view(template_name='forgot-password.html')),
    path("__debug__/", include("debug_toolbar.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

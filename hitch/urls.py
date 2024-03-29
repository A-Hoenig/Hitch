"""
URL configuration for hitch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordChangeView
from django.urls import path, include
from rides import views
from hitch import settings

   
urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('', views.about, name='about'),
    path('rides/', views.rides_view, name='rides_view'),
    path('about/', views.about, name='about'),
    path('hitches/', views.hitches, name='hitches'),
    path('user_profile/', views.profile, name='user_profile'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('locations/', views.locations, name='locations'),
    path('message_center/', views.message_center, name='message_center'),
    path('user_trips/', views.user_trips, name='user_trips'),
    path('change-password/', PasswordChangeView.as_view(), name='password_change'),
]
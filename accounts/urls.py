
from django.contrib import admin
from django.urls import path,include
from .views import register,logout,login


urlpatterns = [
    path('register/', register,name='register'),
    path('logout/',logout,name='logout'),
    path('login/',login,name='signin'),
]

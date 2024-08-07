
from django.contrib import admin
from django.urls import path,include
from .views import register,logout,login,dashboard


urlpatterns = [
    path('register/', register,name='register'),
    path('logout/',logout,name='logout'),
    path('login/',login,name='signin'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    # path('activate/<uidb64>/<token>/', activate, name='activate'), -- in case email verification


]


from django.contrib import admin
from django.urls import path,include
from .views import register,logout,login,dashboard,my_orders,edit_profile,change_password,order_detail


urlpatterns = [
    path('register/', register,name='register'),
    path('logout/',logout,name='logout'),
    path('login/',login,name='signin'),
    path('dashboard/',dashboard,name='dashboard'),
    path('',dashboard,name='dashboard'),
    path('my_orders/',my_orders,name='my_orders'),
    path('edit_profile/',edit_profile,name='edit_profile'),
    path('change_password/',change_password,name='change_password'),
    path('order_detail/<int:order_id>/',order_detail,name='order_detail'),

    
    # path('activate/<uidb64>/<token>/', activate, name='activate'), -- in case email verification


]

from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegisterationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,username=username)
            user.save()
            messages.success(request,'User Created succsufully')
            return redirect('register')
    else:
        form = RegisterationForm()

    return render(request,'accounts/register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        user = auth.authenticate(phone_number=phone_number,password=password)

        if user is not None:
            auth.login(request,user)
            # messages.success(request,'You are now logged in')
            return redirect('home')
        else:
            messages.error(request,'invlaid login credential')
            return redirect('signin')
    return render(request,'accounts/signin.html')

@login_required(login_url = '')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('signin')


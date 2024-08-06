from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    
    if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                # USER CREATION
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone_number = form.cleaned_data['phone_number']
                email = form.cleaned_data['email']
                password = form.cleaned_data['password'] #to validate password and confirm password in def clean(self) later in form.py and used to create user here
                username = email.split('@')[0]
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email,phone_number=phone_number,
                                                username=username, password=password)
                user.phone_number = phone_number
                user.save()
                messages.success(request,'User Created succsufully')
                return redirect('register')
    else:
        form = RegistrationForm()

    return render(request,'accounts/register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)

        if user is not None:
            auth.login(request,user)
            # messages.success(request,'You are now logged in')
            return redirect('home')
        else:
            messages.error(request,'invlaid login credential')
            return redirect('signin')
    return render(request,'accounts/signin.html')

@login_required(login_url = 'signin')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('signin')


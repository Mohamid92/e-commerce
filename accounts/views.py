from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from .forms import RegistrationForm,UserForm,UserProfileForm
from .models import Account,UserProfile
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from cart.views import _cart_id,Cart ,CartItem
import requests
from orders.models import Order,OrderProduct
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
                user.is_active = True
                user.save()
                messages.success(request, 'You have been registered! please log in to activate your account.')
                login_url = reverse('signin')
                return redirect(f'{login_url}?command=successful')
               
                

                # USER ACTIVATION - EMAIL - if it's working - check def activate(request) also
                # current_site = get_current_site(request)
                # domain = current_site.domain 
                # mail_subject = 'ALATA store Activation'
                # message = render_to_string('accounts/account_verification_email.html',{
                #     'user': user,
                #     'domain':domain,
                #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': default_token_generator.make_token(user),
                # })
                # to_email = email
                # send_email = EmailMessage(mail_subject,message,to=[to_email])
                # send_email.send()
                # messages.success(request,'Registeration successful.')
                
                
                
    else:
        form = RegistrationForm()

    return render(request,'accounts/register.html',{'form':form})

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,password=password)
       
        if user is not None:
            try:
                print(f'you are here and cart id is { _cart_id(request)}')
                cart = Cart.objects.get(cart_id=_cart_id(request))

                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    # getting product variations by cart id
                    product_variation = []
                    for item in cart_item:
                        variation= item.variations.all()
                        product_variation.append(list(variation))
                    #  get the cart items from the user to access his product variations
                    cart_item = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id=[]
                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index=ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()

            except:
                pass
            auth.login(request,user)
            messages.success(request,'You are now logged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)                
            except:
                return redirect('dashboard')
        else:
            messages.error(request,'invlaid login credential')
            return redirect('signin')
    return render(request,'accounts/signin.html')

@login_required(login_url = 'signin')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are logged out')
    return redirect('signin')



############################################################################
#####################If there's Email activating############################
############################################################################
# def activate(request):
#             # def activate(request,uidb64,token):
#                 # try:
#                 #     uid = urlsafe_base64_decode(uidb64).decode()
#                 #     user = Account._default_manager.get(pk=uid)
#                 # except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
#                 #     user = None

#                 #     if user is not None and default_token_generator.check_token(user,token):
#                 #         user.is_activate = True
#                 #         user.save()
#                 #         messages.success(request,'Congratulations! your account is activated.')
#                 #         return redirect('signin')
#                 #     else:
#                 #         messages.error(request,'Invalid activation link')
#                 #         return redirect('register')
#             user = request.user
#             print('this is under active:   ',user)
#             user.is_activate = True
#             user.save()
#             messages.success(request,'Congratulations! your account is activated.')
#             return redirect('signin')


@login_required(login_url='login')
def dashboard(request):
    print(request.path)
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id,is_ordered=True)
    orders_count = orders.count()
    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count':orders_count,
        'userprofile':userprofile
    }
    return render(request,'accounts/dashboard.html',context)

@login_required(login_url='login')
def my_orders(request):
    print(request.path)
    orders = Order.objects.filter(user=request.user,  is_ordered=True).order_by('-created_at')
    context = {
        'orders':orders,
    }
    return render(request,'accounts/my_orders.html',context)

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('edit_profile')
        else:
            print("User Form Errors:", user_form.errors)
            print("Profile Form Errors:", profile_form.errors)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request,'password was changed')
                return redirect('change_password')
            else:
                messages.error(request,'current password is not correct')
                return redirect('change_password')
            
    return render(request,'accounts/change_password.html')

@login_required(login_url='login')
def order_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity
    context= {
        'order_detail':order_detail,
        'order':order,
    }
    return render(request,'accounts/order_detail.html',context)
    
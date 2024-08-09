from django.shortcuts import render, redirect
from store.models import Product,Variation
from .models import Cart, CartItem
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def _cart_id(request):
    # Get the current session key
    print('reaching herec cart id')
    cart = request.session.get('cart_id', None)
    
    # If no session key exists, create a new one
    if not cart:
        # Save the session to ensure it has a session_key
        request.session.create()  # Create a new session
        cart = request.session.session_key
        # Save the cart_id in the session
        request.session['cart_id'] = cart

    return cart

def add_cart(request, product_id):
    current_user=request.user
    product = Product.objects.get(id=product_id)
    #if the user is authenticated
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,
                                                    variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        

    
        # cart_id = _cart_id(request)

       


        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,user=current_user)
            ex_var_list = []
            id=[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            print(ex_var_list)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
            
            else:
                item = CartItem.objects.create(product=product,quantity=1,user=current_user)
                if len(product_variation) > 0 :
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user
            )
            if len(product_variation) > 0 :
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')
   
    else:
        product_variation = []
        if request.method == 'POST':
            
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                
                try:
                    variation = Variation.objects.get(product=product,variation_category__iexact=key,
                                                    variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass
        

    
        cart_id = _cart_id(request)

        try:
            # Attempt to retrieve the Cart
            cart = Cart.objects.get(cart_id=cart_id)
        except Cart.DoesNotExist:
            # Create a new Cart if it does not exist
            cart = Cart.objects.create(cart_id=cart_id)

        cart_item = None


        is_cart_item_exists = CartItem.objects.filter(product=product,cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product,cart=cart)
            ex_var_list = []
            id=[]
            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)
            
            print(ex_var_list)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product,id=item_id)
                item.quantity += 1
                item.save()
            
            else:
                item = CartItem.objects.create(product=product,quantity=1,cart=cart)
                if len(product_variation) > 0 :
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )
            if len(product_variation) > 0 :
                    cart_item.variations.clear()
                    cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    delete = request.GET.get('delete', None)
    
    product = Product.objects.get(id=product_id)
    try: 
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product , user=request.user,id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product , cart = cart,id=cart_item_id)
        if delete == 'true':
            cart_item.delete()
        elif cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect('cart')
    
def cart(request,total=0,quantity=0,cart_items=None):
    cart_id =_cart_id(request)
    print(f'start of cart function :::  {cart_id}')

    try:
        if request.user.is_authenticated:
            cartitems = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id=cart_id)
            cartitems = CartItem.objects.filter(cart=cart,is_active=True)
        print(f'finding cart items :::  {cartitems}')
        for items in cartitems:
            total += (items.product.price * items.quantity)
            quantity += items.quantity
        tax = ( 2* total)/100
        grand_total = tax + total
        
        context = {
            'total' : total,
            'quantity' : quantity,
            'cart_items' : cartitems,
            'tax':tax,
            'grand_total':grand_total
        }
    except Cart.DoesNotExist:
        cartitems = []  # or handle the case where the cart does not exist

    context = {'cart_items' : cartitems}
    return render(request, 'cart/cart.html',context)

@login_required(login_url='signin')
def checkout(request,total=0,quantity=0,cart_items=None):
    cart_id =_cart_id(request)

    if request.user.is_authenticated:
            cartitems = CartItem.objects.filter(user=request.user,is_active=True)
    else:
            cart = Cart.objects.get(cart_id=cart_id)
            cartitems = CartItem.objects.filter(cart=cart,is_active=True)


    # 


    for items in cartitems:
        total += (items.product.price * items.quantity)
        quantity += items.quantity
    tax = ( 2* total)/100
    grand_total = tax + total
    
    context = {
        
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cartitems,
        'tax':tax,
        'grand_total':grand_total
    }
    return render(request,'cart/checkout.html',context)
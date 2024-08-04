from django.shortcuts import render, redirect
from store.models import Product,Variation
from .models import Cart, CartItem
from django.http import HttpResponse

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()  # Use request.session.save() to ensure session creation        
        cart = request.session.session_key
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
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
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try: 
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
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cartitems = CartItem.objects.filter(cart=cart,is_active=True)
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
    return render(request, 'cart/cart.html',context)
from django.shortcuts import render, redirect
from store.models import Product
from .models import Cart, CartItem

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        request.session.create()  # Use request.session.save() to ensure session creation        
        cart = request.session.session_key
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_id = _cart_id(request)

    try:
        # Attempt to retrieve the Cart
        cart = Cart.objects.get(cart_id=cart_id)
    except Cart.DoesNotExist:
        # Create a new Cart if it does not exist
        cart = Cart.objects.create(cart_id=cart_id)

    try:
        # Attempt to retrieve the CartItem
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        # Create a new CartItem if it does not exist
        CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )

    return redirect('cart')

def remove_cart(request,product_id):
    delete = request.GET.get('delete', None)
    
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_item = CartItem.objects.get(product=product , cart = cart)

    if delete == 'true':
        cart_item.delete()
    elif cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
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
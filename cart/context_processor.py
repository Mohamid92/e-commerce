from .models import Cart,CartItem
from .views import _cart_id
def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    else : 
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            if request.user.is_authenticated:
                cart_count = CartItem.objects.all().filter(user=request.user).count()
            else:
                cart_count = CartItem.objects.filter(cart=cart).count()
            
        except Cart.DoesNotExist:
            cart_count = 0

        return {'cart_count': cart_count}
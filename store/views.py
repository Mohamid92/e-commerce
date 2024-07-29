from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator

# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None

    
    if category_slug != None :
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(Category=categories , is_available=True)
        
    else :
        products = Product.objects.all().filter(is_available=True).order_by('-id')

    paginator = Paginator(products,6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'products': page_obj.object_list,
        'page_obj':page_obj,
    }
    
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    # product_detail = get_object_or_404(Product,slug=product_slug)
    try:
        product_detail = Product.objects.get(Category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request),product=product_detail).exists()
    except Exception as e:
        raise e
    
    context = {
        'product_detail':product_detail,
        'in_cart':in_cart
    }
    return render(request,'store/product-detail.html',context)
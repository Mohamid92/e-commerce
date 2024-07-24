from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
# Create your views here.

def store(request,category_slug=None):
    categories = None
    products = None
    
    if category_slug != None :
        categories = get_object_or_404(Category,slug=category_slug)
        products = Product.objects.filter(Category=categories , is_available=True)
        
    else :
        products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    # product_detail = get_object_or_404(Product,slug=product_slug)
    try:
        product_detail = Product.objects.get(Category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    
    context = {
        'product_detail':product_detail
    }
    return render(request,'store/product-detail.html',context)
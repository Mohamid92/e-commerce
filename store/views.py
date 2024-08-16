from django.shortcuts import render,get_object_or_404,redirect
from .models import Product ,ReviewRating,ProductGallery
from category.models import Category
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from orders.models import OrderProduct
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
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user,product_id=product_detail.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Gt the reviews
    reviews = ReviewRating.objects.filter(product_id=product_detail.id,status=True)
    # get the product the gallery
    product_gallery = ProductGallery.objects.filter(product_id=product_detail.id)
    context = {
        'product_detail':product_detail,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews':reviews,
        'product_gallery':product_gallery
    }
    return render(request,'store/product-detail.html',context)


def search(request):
          keyword = request.GET.get('keyword')
          products = []
          product_count = 0
    
          if keyword:
                products = Product.objects.filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
                product_count = products.count()

          context = {
                'products': products,
                'product_count': product_count,
                'keyword': keyword  # Optional: Pass keyword back to the template for displaying in the search input
            }
        
          return render(request, 'store/store.html', context)


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')  # Get the previous URL to redirect back
    if request.method == 'POST':
        # Try to get an existing review by the user and product
        try:
            review = ReviewRating.objects.get(user_id=request.user.id, product_id=product_id)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank You! Your review was updated')
                return redirect(url)
        except ReviewRating.DoesNotExist:
            # Create a new review if none exists
            form = ReviewForm(request.POST)
            if form.is_valid():
                new_review = form.save(commit=False)
                new_review.product_id = product_id  # Set the product_id
                new_review.user_id = request.user.id  # Set the user_id
                new_review.ip = request.META.get('REMOTE_ADDR')  # Set the IP address
                new_review.save()
                messages.success(request, 'Thank You! Your review has been submitted')
                return redirect(url)
    return redirect(url) 
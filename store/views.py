from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product
from django.db.models import Q
from category.models import Category
from carts.models import Cart, CartItem
from carts.utils import _cart_id
from base.utils import _number

# Create your views here.
def store(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    products = Product.objects.filter(
        Q(slug__icontains=q) |
        Q(product_name__icontains=q) |
        Q(category__category_name__icontains=q), is_available=True
    ).order_by('id')
    
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj =  paginator.get_page(page_number)
    
    categories = Category.objects.all()

    context = {
        "categories": categories, 
        'number': _number(request),
        'page_obj': page_obj,   
        'products': products,
        'page_number': page_number
    }
    return render(request, 'store.html', context)

def productDetail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product)
    except Product.DoesNotExist:
        return redirect('home')
    
    categories = Category.objects.all()
    
    context = {
        "categories": categories,
        'product': product, 
        "in_cart": in_cart,
        'number': _number(request)
    }
    return render(request, 'product-detail.html', context)
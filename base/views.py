from django.shortcuts import render
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from store.models import Product
from django.db.models import Q
from category.models import Category
from .utils import _number


# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ""
    products = Product.objects.filter(
        Q(slug__icontains=q) |
        Q(product_name__icontains=q) |
        Q(category__category_name__icontains=q), is_available=True
    )

    categories = Category.objects.all()
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': products, 
        "categories": categories,
        'number': _number(request),
        'page_obj': page_obj
    }
    return render(request, 'store.html', context)

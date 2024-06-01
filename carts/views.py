from django.shortcuts import render, redirect
from store.models import Product, Variation
from .models import Cart, CartItem
from .utils import _cart_id
from base.utils import _number
from category.models import Category

# Create your views here.


def cart(request, total=0, tax=0):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))

    for items in cart_items:
        total += int(items.product.price) * items.quantity

    tax = 10
    grandTotal = total + tax

    categories = Category.objects.all()

    context = {
        "categories": categories,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grandTotal': grandTotal,
        'number': _number(request)
    }
    return render(request, 'cart.html', context)


def add_cart(request, pk):

    product = Product.objects.get(id=pk)
    product_variation = []

    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]

            try:
                variation = Variation.objects.get(
                    variation_category__iexact=key,
                    variation_value__iexact=value,
                    product=product
                )

                product_variation.append(variation)
                print(product_variation)
            except Variation.DoesNotExist:
                pass

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for val in product_variation:
                cart_item.variation.add(val)
        
        cart_item.quantity += 1

        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for val in product_variation:
                cart_item.variation.add(val)
                
        cart_item.save()

    return redirect('cart')


def reduce_quantity(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(cart_id=_cart_id(request))
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity -= 1
        cart_item.save()

        if cart_item.quantity <= 0:
            cart_item.delete()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )

    return redirect('cart')


def remove(request, pk):
    product = Product.objects.get(id=pk)
    cart = Cart.objects.get(cart_id=_cart_id(request))

    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')

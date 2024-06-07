from carts.utils import _cart_id
from carts.models import CartItem



def _number(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.all().filter(user=request.user)
    else:
        cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    return cart_items.count

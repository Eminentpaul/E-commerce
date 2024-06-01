from carts.utils import _cart_id
from carts.models import CartItem



def _number(request):
    cart_items = CartItem.objects.filter(cart__cart_id=_cart_id(request))
    return cart_items.count

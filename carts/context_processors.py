from .models import Cart,CartItem
from .views import _cart_id

def cart_counter(request):
    if 'admin' in request.path:
        return {}
    else:
        counter=0
        try:
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cartItems=CartItem.objects.filter(cart=cart)
            for item in cartItems:
                 counter+=item.quantity
        except Cart.DoesNotExist:
                pass
        return dict(cart_counter=counter)
            
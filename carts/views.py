from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Cart,CartItem
from store.models import Product


# Create your views here.



def _cart_id(request):
    cartID=request.session.session_key
    if not cartID:
        cartID=request.session.create()
    return cartID


def AddToCart(request,product_id):
    product=get_object_or_404(Product,id=product_id)

    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist :
        cart=Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cartitem=CartItem.objects.get(product=product,cart=cart)
        cartitem.quantity+=1
        cartitem.save()
    except CartItem.DoesNotExist:
        cartitem=CartItem.objects.create(product=product,cart=cart,quantity=1)    
        cartitem.save()

    return redirect('cart')   



def remove_cart(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=get_object_or_404(CartItem,product=product,cart=cart)
    if cart_item.quantity>1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')    

def remove_cart_item(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=get_object_or_404(CartItem,product=product,cart=cart)
    cart_item.delete()

    return redirect('cart')    


def cart(request,total=0,quantity=0,cart_items=None,tax=0,grand_total=0):
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for item in cart_items:
            total+=(item.product.price * item.quantity)
            quantity+=item.quantity

        tax=round((2*total)/100,2)
        grand_total=total+tax    

    except Cart.DoesNotExist:
        pass
    context={'total':total,
             'quantity':quantity,
             'tax':tax,
             'grand_total':grand_total,
              'cart_items'  :cart_items      
             }

    return render(request,'store/cart.html',context)



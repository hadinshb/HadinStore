from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
def store(request,category_slug=None):
    category=None;
    products=None;
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.all().filter(is_available=True,category=category).order_by('id')
    else:    
        products=Product.objects.all().filter(is_available=True).order_by('id')

    prodoct_count=products.count()   
        
    paginator=Paginator(products,6)    
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)

    context={'products':paged_product,'prodoct_count':prodoct_count}
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    single_product=get_object_or_404(Product,slug=product_slug,category__slug=category_slug)
    in_cart=CartItem.objects.filter(product=single_product,cart__cart_id=_cart_id(request)).exists()

    context={'product':single_product,'in_cart':in_cart}
    return render(request,'store/product_details.html',context)


def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
        prodoct_count=products.count()   

    paginator=Paginator(products,6)    
    page=request.GET.get('page')
    paged_product=paginator.get_page(page)      
    context={'products':paged_product,'prodoct_count':prodoct_count}
    return render(request,'store/store.html',context)

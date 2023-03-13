from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import Product
from category.models import Category

# Create your views here.
def store(request,category_slug=None):
    category=None;
    products=None;
    if category_slug:
        category=get_object_or_404(Category,slug=category_slug)
        products=Product.objects.all().filter(is_available=True,category=category)
    else:    
        products=Product.objects.all().filter(is_available=True)
    context={'products':products}
    return render(request,'store/store.html',context)

def product_details(request,category_slug,product_slug):
    single_product=get_object_or_404(Product,slug=product_slug,category__slug=category_slug)
    context={'product':single_product}
    return render(request,'store/product_details.html',context)

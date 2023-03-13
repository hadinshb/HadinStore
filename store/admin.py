from django.contrib import admin
from .models import Product
from django.contrib.admin import ModelAdmin


class ProductAdmin(ModelAdmin):
    list_display=('product_name','price','stock','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}


# Register your models here.
admin.site.register(Product,ProductAdmin)
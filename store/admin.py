from django.contrib import admin
from .models import Product,variation
from django.contrib.admin import ModelAdmin


class ProductAdmin(ModelAdmin):
    list_display=('product_name','price','stock','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}

class VariationAdmin(ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value')
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(variation,VariationAdmin)
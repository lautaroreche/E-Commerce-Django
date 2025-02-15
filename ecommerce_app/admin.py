from django.contrib import admin
from ecommerce_app.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')
    search_fields = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')

admin.site.register(Product, ProductAdmin)

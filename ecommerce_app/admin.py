from django.contrib import admin
from ecommerce_app.models import Product, Order, Payment, SuscriptorNewsletter
from django.contrib.sessions.models import Session


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')
    list_filter = ('category',)
    search_fields = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_products', 'total', 'address', 'date', 'status', 'payment')
    list_filter = ('status',)
    search_fields = ('id', 'products', 'total', 'address', 'date', 'status', 'payment')
    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = 'Products'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'method', 'detail', 'amount', 'date', 'status', 'order')
    list_filter = ('method', 'status',)
    search_fields = ('id', 'order', 'method', 'detail', 'amount', 'date', 'status', 'order')


class SuscriptorNewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')


admin.site.register(Session)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(SuscriptorNewsletter, SuscriptorNewsletterAdmin)

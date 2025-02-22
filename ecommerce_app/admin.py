from django.contrib import admin
from ecommerce_app.models import Product, User, Order, Payment
from django.contrib.sessions.models import Session


admin.site.register(Session)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')
    search_fields = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'city', 'state', 'zip_code')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'city', 'state', 'zip_code')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_products', 'total', 'address', 'date', 'status', 'payment')
    search_fields = ('id', 'user', 'products', 'total', 'address', 'date', 'status', 'payment')
    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = 'Products'


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'method', 'detail', 'amount', 'date', 'status', 'order')
    search_fields = ('id', 'user', 'order', 'method', 'detail', 'amount', 'date', 'status', 'order')


admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)

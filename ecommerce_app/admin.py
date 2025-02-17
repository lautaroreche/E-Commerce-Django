from django.contrib import admin
from ecommerce_app.models import Product, User, Order, Review, Payment, Shipping


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')
    search_fields = ('id', 'name', 'price', 'description', 'image', 'category', 'stock')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'city', 'state', 'zip_code')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'city', 'state', 'zip_code')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_products', 'total', 'address', 'date', 'status')
    search_fields = ('id', 'user', 'products', 'total', 'address', 'date', 'status')
    def get_products(self, obj):
        return ", ".join([p.name for p in obj.products.all()])
    get_products.short_description = 'Products'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'comment', 'date')
    search_fields = ('id', 'user', 'product', 'rating', 'comment', 'date')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'order', 'payment_method', 'amount', 'date', 'status')
    search_fields = ('id', 'user', 'order', 'payment_method', 'amount', 'date', 'status')


class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'address', 'date', 'status')
    search_fields = ('id', 'order', 'address', 'date', 'status')


admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Shipping, ShippingAdmin)

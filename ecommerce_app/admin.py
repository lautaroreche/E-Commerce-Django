from django.contrib import admin
from ecommerce_app.models import Product, SuscriptorNewsletter
from django.contrib.sessions.models import Session


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'description', 'category', 'is_top_of_category', 'is_trend')
    list_filter = ('category', 'is_top_of_category', 'is_trend')
    search_fields = ('name', 'price', 'description', 'category')

class SuscriptorNewsletterAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    search_fields = ('id', 'email')


admin.site.register(Session)
admin.site.register(Product, ProductAdmin)
admin.site.register(SuscriptorNewsletter, SuscriptorNewsletterAdmin)

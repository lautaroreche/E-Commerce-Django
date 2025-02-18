from django.shortcuts import redirect
from django.http import HttpResponse
from ecommerce_app.models import Product
from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id = product_id)
    cart.add(product)
    return redirect("/home/")


def remove_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id = product_id)
    cart.remove(product)
    return redirect("/home/")


def decrement_product_from_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id = product_id)
    cart.decrement(product)
    return redirect("/home/")


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/home/")

from django.shortcuts import redirect
from .cart import Cart


def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def decrement_from_cart(request, product_id):
    cart = Cart(request)
    cart.decrement(product_id)
    return redirect(request.META.get('HTTP_REFERER', '/'))


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(request.META.get('HTTP_REFERER', '/'))

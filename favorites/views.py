from django.shortcuts import redirect
from ecommerce_app.models import Product
from .favorites import Favorites
from cart.views import Cart


def add_to_favorites(request, product_id):
    favorites = Favorites(request)
    product = Product.objects.get(id = product_id)
    favorites.add(product)
    return redirect("/home/")


def remove_from_favorites(request, product_id):
    favorites = Favorites(request)
    product = Product.objects.get(id = product_id)
    favorites.remove(product)
    return redirect("/home/")


def clear_favorites(request):
    favorites = Favorites(request)
    favorites.clear()
    return redirect("/home/")


def add_all_favorites_to_cart(request):
    favorites = Favorites(request)
    cart = Cart(request)
    for key, value in favorites.get_all():
        product = Product.objects.get(id = key)
        cart.add(product)
    return redirect("/cart/")

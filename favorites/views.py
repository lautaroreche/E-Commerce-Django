from django.shortcuts import redirect
from .favorites import Favorites
from cart.views import Cart


def manage_favorites(request, product_id):
    favorites = Favorites(request)
    favorites.manage(product_id)
    return redirect("/home/")


def clear_favorites(request):
    favorites = Favorites(request)
    favorites.clear()
    return redirect("/home/")


def add_all_favorites_to_cart(request):
    favorites = Favorites(request)
    cart = Cart(request)
    for product_id in favorites.favorites:
        cart.add(product_id)
    return redirect("/cart/")

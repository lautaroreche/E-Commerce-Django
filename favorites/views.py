from django.shortcuts import render, redirect
from django.http import HttpResponse
from ecommerce_app.models import Product
from .favorites import Favorites


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

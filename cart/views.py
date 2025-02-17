from django.shortcuts import render, redirect
from django.http import HttpResponse
from ecommerce_app.models import Product
from .cart import Cart


def add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product)
    return redirect("/home/")

def remove(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect("/home/")

def decrement(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.decrement(product)
    return redirect("/home/")

def clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("/home/")
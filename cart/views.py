from django.shortcuts import render
from cart import Cart
from ecommerce_app.models import Product
from django.shortcuts import HttpResponseRedirect


def agregar(request, product_id):
    
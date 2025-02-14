from django.shortcuts import render
from ecommerce_app.models import Product


def base(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, 'base.html', {'categories': categories})


def home(request):
    items = Product.objects.all()
    return render(request, 'home.html', {'items': items})

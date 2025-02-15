from django.shortcuts import render
from ecommerce_app.models import Product
from django.http import HttpResponse


def base(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, 'base.html', {
        "categories": categories,
    })


def home(request):
    productos = Product.objects.all()
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, 'home.html', {
        "productos": productos,
        "categories": categories,
    })


def search(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    if request.method == "POST":
        nombre_producto = request.POST.get("nombre_producto", "").strip()
        if not nombre_producto:
            return render(request, "error.html", {
                "error": "No has introducido ningún artículo",
                'categories': categories,
            })
        if len(nombre_producto) > 20:
            return render(request, "error.html", {
                "error": "Texto de búsqueda demasiado largo. Por favor, introduce un texto más corto",
                'categories': categories,
            })
        productos = Product.objects.filter(name__icontains=nombre_producto)
        return render(request, "search.html", {
            "productos": productos,
            "resultados": len(productos),
            "query": nombre_producto,
            "categories": categories,
        })
    return HttpResponse("Método no permitido")


def filter(request, category):
    productos = Product.objects.filter(category=category)
    categories = Product.objects.values('category').distinct().order_by('category')
    if not productos:
        return render(request, "error.html", {
            "error": "La categoría que acabas de buscar no existe",
            'categories': categories,
        })
    return render(request, "filter.html", {
        "productos": productos,
        "resultados": len(productos),
        "category": category,
        "categories": categories,
    })


def account(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, 'account.html', {
        "categories": categories,
    })


def cart(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, 'cart.html', {
        "categories": categories,
    })

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
import smtplib
from email.mime.text import MIMEText
from ecommerce.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_SENDER_NAME, EMAIL_SUBJECT
from ecommerce_app.models import Product
from cart.cart import Cart
from favorites.favorites import Favorites
from ecommerce_app.forms import FormularioNewsletter


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
            messages.error(request, "No has buscado ningún producto")
            messages.info(request, "Escribe el nombre de algún producto en la barra de búsqueda")
            return redirect("/error/")
        if len(nombre_producto) > 20:
            messages.error(request, "Nombre de producto demasiado largo")
            messages.info(request, "Introduce un nombre de producto más corto")
            return redirect("/error/")
        productos = Product.objects.filter(name__icontains=nombre_producto)
        if not productos:
            messages.error(request, f'No hay ningún producto similar a "{nombre_producto}"')
            messages.info(request, "Intenta buscar el producto de otra forma, o busca otro producto")
            return redirect("/error/")
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
        messages.error(request, "La categoría que acabas de buscar no existe")
        messages.info(request, "Intenta seleccionar otra categoría")
        return redirect("/error/")
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
    cart_obj = Cart(request)
    return render(request, 'cart.html', {
        "categories": categories,
        "subtotal_dict": cart_obj.get_total_product(),
        "total": str(cart_obj.get_total_cart()),
    })


def favorites(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    cart_obj = Cart(request)
    return render(request, 'favorites.html', {
        "categories": categories,
        "subtotal_dict": cart_obj.get_total_product(),
    })


def newsletter(request):
    form = FormularioNewsletter(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]

        html_content = render_to_string("newsletter_message.html")
        msg = MIMEText(html_content, "html")
        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = f"{EMAIL_SENDER_NAME} <{EMAIL_HOST_USER}>"
        msg["To"] = email

        try:
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                server.sendmail(EMAIL_HOST_USER, email, msg.as_string())
                messages.success(request, "Te has suscripto a nuestro newsletter exitosamente")
                messages.info(request, "En breve recibirás un email de confirmación")
                return redirect("/congrats/")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")
            messages.info(request, "Intenta nuevamente en unos minutos")
            return redirect("/error/")
    messages.error(request, "El email ingresado no es válido")
    messages.info(request, "Ingresa un email válido")
    return redirect("/error/")


def error(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, "error.html", {
        "categories": categories,
    })


def congrats(request):
    categories = Product.objects.values('category').distinct().order_by('category')
    return render(request, "congrats.html", {
        "categories": categories,
    })

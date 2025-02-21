from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
import smtplib
from email.mime.text import MIMEText
from ecommerce.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_SENDER_NAME
from ecommerce_app.models import Product
from cart.cart import Cart
from favorites.favorites import Favorites
from ecommerce_app.forms import FormularioNewsletter


CATEGORIES = Product.objects.values('category').distinct().order_by('category')


def base(request):
    return render(request, 'base.html', {
        "categories": CATEGORIES,
    })


def home(request):
    productos = Product.objects.all()
    favorites_obj = Favorites(request)
    cart_obj = Cart(request)
    return render(request, 'home.html', {
        "productos": productos,
        "categories": CATEGORIES,
        "productos_favoritos": favorites_obj.get_list_items(),
        "productos_cart": cart_obj.get_list_items(),
    })


def search(request):
    if request.method == "POST":
        nombre_producto = request.POST.get("nombre_producto", "").strip()
        if not nombre_producto:
            messages.error(request, "No has buscado ningún producto")
            messages.info(request, "Escribe el nombre de algún producto en la barra de búsqueda")
            return redirect("/feedback/")
        if len(nombre_producto) > 20:
            messages.error(request, "Nombre de producto demasiado largo")
            messages.info(request, "Introduce un nombre de producto más corto")
            return redirect("/feedback/")
        productos = Product.objects.filter(name__icontains=nombre_producto)
        if not productos:
            messages.error(request, f'No hay ningún producto similar a "{nombre_producto}"')
            messages.info(request, "Intenta buscar el producto de otra forma, o busca otro producto")
            return redirect("/feedback/")
        return render(request, "search.html", {
            "productos": productos,
            "resultados": len(productos),
            "query": nombre_producto,
            "categories": CATEGORIES,
        })
    return HttpResponse("Método no permitido")


def filter(request, category):
    productos = Product.objects.filter(category=category)
    if not productos:
        messages.error(request, "La categoría que acabas de buscar no existe")
        messages.info(request, "Intenta seleccionar otra categoría")
        return redirect("/feedback/")
    return render(request, "filter.html", {
        "productos": productos,
        "resultados": len(productos),
        "category": category,
        "categories": CATEGORIES,
    })


def cart(request):
    cart_obj = Cart(request)
    productos_cart = cart_obj.get_list_items()
    productos = Product.objects.filter(id__in=productos_cart)
    if productos:
        return render(request, 'cart.html', {
            "categories": CATEGORIES,
            "productos": productos,
            "productos_cart": productos_cart,
            "is_cart": True,
            "subtotal_dict": cart_obj.get_total_product(),
            "total": str(cart_obj.get_total_cart()),
        })
    messages.warning(request, "No tienes ningún producto en el carrito")
    messages.info(request, "Haz click en el símbolo + de color verde  que se encuentra en el producto para que aparezca aquí")
    return redirect("/feedback/")


def favorites(request):
    cart_obj = Cart(request)
    favorites_obj = Favorites(request)
    productos_favoritos = favorites_obj.get_list_items()
    productos = Product.objects.filter(id__in=productos_favoritos)
    if productos:
        return render(request, 'favorites.html', {
            "categories": CATEGORIES,
            "productos": productos,
            "productos_cart": cart_obj.get_list_items(),
            "is_cart": False,
        })
    messages.warning(request, "No tienes ningún producto marcado como favorito")
    messages.info(request, "Haz click en el corazón que se encuentra en la imagen del producto para que aparezca aquí")
    return redirect("/feedback/")


def newsletter(request):
    form = FormularioNewsletter(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        html_content = render_to_string("newsletter_message.html")
        msg = MIMEText(html_content, "html")
        msg["Subject"] = "Ragusa - Productos argentinos"
        msg["From"] = f"{EMAIL_SENDER_NAME} <{EMAIL_HOST_USER}>"
        msg["To"] = email
        try:
            with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT) as server:
                server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
                server.sendmail(EMAIL_HOST_USER, email, msg.as_string())
                messages.success(request, "Te has suscripto a nuestro newsletter exitosamente")
                messages.info(request, "En breve recibirás un email de confirmación")
                return redirect("/feedback/")
        except Exception as e:
            messages.error(request, f"Error inesperado: {e}")
            messages.info(request, "Intenta nuevamente en unos minutos")
            return redirect("/feedback/")
    messages.error(request, "El email ingresado no es válido")
    messages.info(request, "Ingresa un email válido")
    return redirect("/feedback/")


def feedback(request):
    storage = messages.get_messages(request)
    if any(storage):
        return render(request, "feedback.html", {
            "categories": CATEGORIES,
        })
    return redirect("/")


def custom_logout(request):
    if request.method == "POST":
        logout(request)
    return redirect('/')

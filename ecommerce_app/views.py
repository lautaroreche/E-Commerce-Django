from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import logout
import smtplib
from email.mime.text import MIMEText
from ecommerce.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_SENDER_NAME
from ecommerce_app.models import Product, SuscriptorNewsletter
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
    cart_obj = Cart(request)
    productos_cart = cart_obj.get_list_items()
    favorites_obj = Favorites(request)
    productos_favoritos = favorites_obj.get_list_items()
    return render(request, 'home.html', {
        "categories": CATEGORIES,
        "productos": productos,
        "productos_cart": productos_cart,
        "productos_favoritos": productos_favoritos,
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
        # No cumple ningún caso mapeado así que es un redirect desde add fav o add cart, guardamos el nombre del producto para lo siguiente
        request.session["nombre_producto"] = nombre_producto
    
    try:
        # Viene de redirect cuando se agrega producto a fav o cart, así que cargamos de nuevo la misma página
        nombre_producto = request.session.get('nombre_producto', '')
        productos = Product.objects.filter(name__icontains=nombre_producto)
        cart_obj = Cart(request)
        productos_cart = cart_obj.get_list_items()
        favorites_obj = Favorites(request)
        productos_favoritos = favorites_obj.get_list_items()
        return render(request, "search.html", {
            "categories": CATEGORIES,
            "productos": productos,
            "productos_cart": productos_cart,
            "productos_favoritos": productos_favoritos,
            "resultados": len(productos),
            "query": nombre_producto,
        })
    except:
        return redirect('/')


def filter(request, category):
    productos = Product.objects.filter(category=category)
    if not productos:
        messages.error(request, "La categoría que acabas de buscar no existe")
        messages.info(request, "Intenta seleccionar otra categoría")
        return redirect("/feedback/")
    cart_obj = Cart(request)
    productos_cart = cart_obj.get_list_items()
    favorites_obj = Favorites(request)
    productos_favoritos = favorites_obj.get_list_items()
    return render(request, "filter.html", {
        "categories": CATEGORIES,
        "productos": productos,
        "productos_cart": productos_cart,
        "productos_favoritos": productos_favoritos,
        "resultados": len(productos),
        "category": category,
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
    productos_cart = cart_obj.get_list_items()
    favorites_obj = Favorites(request)
    productos_favoritos = favorites_obj.get_list_items()
    productos = Product.objects.filter(id__in=productos_favoritos)
    if productos:
        return render(request, 'favorites.html', {
            "categories": CATEGORIES,
            "productos": productos,
            "productos_cart": productos_cart,
            "is_cart": False,
        })
    messages.warning(request, "No tienes ningún producto marcado como favorito")
    messages.info(request, "Haz click en el corazón que se encuentra en la imagen del producto para que aparezca aquí")
    return redirect("/feedback/")


def newsletter(request):
    # Redirect forzado ya que actualmente no se envían mails de newsletter
    messages.warning(request, "Sección en pausa")
    messages.info(request, "Actualmente no se envían mails de newsletter, pero te invitamos a seguir buscando productos")
    return redirect("/feedback/")
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
                suscriptor_newsletter = SuscriptorNewsletter(email=email)
                suscriptor_newsletter.save()
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
    messages.warning(request, "Has cerrado sesión")
    messages.info(request, "Esperamos que vuelvas pronto")
    return redirect("/feedback/")


def checkout(request):
    messages.warning(request, "Sección en construcción")
    messages.info(request, "Estamos desarrollando esta sección así te esperamos nuevamente cuando esté finalizada")
    return redirect("/feedback/")

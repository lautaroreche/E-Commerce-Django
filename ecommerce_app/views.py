from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
import smtplib
from email.mime.text import MIMEText
from ecommerce.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_SENDER_NAME, BREVO_API_KEY
from ecommerce_app.models import Product, SuscriptorNewsletter, Order, OrderItem
from cart.cart import Cart
from favorites.favorites import Favorites
from ecommerce_app.forms import FormularioNewsletter
import sib_api_v3_sdk


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


def detail(request, product_id):
    producto = Product.objects.get(id=product_id)
    if producto:
        cart_obj = Cart(request)
        productos_cart = cart_obj.get_list_items()
        favorites_obj = Favorites(request)
        productos_favoritos = favorites_obj.get_list_items()
        return render(request, 'product_detail.html', {
            "categories": CATEGORIES,
            "producto": producto,
            "productos_cart": productos_cart,
            "productos_favoritos": productos_favoritos,
        })
    messages.error(request, f'No hay ningún producto similar a "{producto.name}"')
    messages.info(request, "Intenta buscar el producto de otra forma, o busca otro producto")
    return redirect("/feedback/")


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
    messages.info(request, "Haz click en el botón verde de Agregar al carrito o en el símbolo + que se encuentran en el producto para que aparezca aquí")
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
    form = FormularioNewsletter(request.POST)
    if form.is_valid():
        email_destino = form.cleaned_data["email"]
        
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        
        api_client = sib_api_v3_sdk.ApiClient(configuration)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
        
        # Renderizar el contenido HTML con contexto si es necesario, o vacío si no
        html_content = render_to_string("newsletter_message.html", {})
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email_destino}],
            sender={"name": "Ragusa - Ecommerce", "email": "lautaroreche1@gmail.com"},
            subject="Gracias por suscribirte",
            html_content=html_content,
        )
        
        try:
            api_instance.send_transac_email(send_smtp_email)
            messages.success(request, "Te has suscripto a nuestro newsletter exitosamente")
            messages.info(request, "En breve recibirás un email de confirmación")
            return redirect("/feedback/")
        except:
            messages.warning(request, "Error en el envío de email")
            messages.info(request, "Intenta nuevamente más tarde")
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


def checkout(request):
    try:
        cart_obj = Cart(request)
        product_list = []
        
        order = Order.objects.create(
            total = cart_obj.get_total_cart(),
            address = "Dirección de prueba 123",
            payment = None,
        )

        for key, value in request.session["cart"].items():
            product = Product.objects.get(id=key)
            quantity = value["quantity"]
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

            product_list.append(product)

        order.products.set(product_list)

        cart_obj.clear()
    
        messages.warning(request, "Funcionalidad actualmente deshabilitada")
        messages.info(request, "El checkout no está habilitado actualmente ya que queda pendiente integrar la pasarela de pagos")
        return redirect("/feedback/")
    except Exception as e:
        print(e)
        messages.error(request, "Error inesperado")
        messages.info(request, "Intenta nuevamente en unos minutos")
        return redirect("/feedback/")

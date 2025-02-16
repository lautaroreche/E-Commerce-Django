from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse
import smtplib
from email.mime.text import MIMEText
from ecommerce.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_SENDER_NAME, EMAIL_SUBJECT
from ecommerce_app.models import Product
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


def newsletter(request):
    categories = Product.objects.values('category').distinct().order_by('category')
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
                return render(request, "congrats.html", {
                    "mensaje": f"Te has suscripto a nuestro newsletter exitosamente {email}",
                    "categories": categories,
                })
        except Exception as e:
            return render(request, "error.html", {
                "error": f"Hay un error inesperado: {e}",
                "categories": categories,
            })
        
    return render(request, "error.html", {
        "error": "El email ingresado no es válido, intenta nuevamente",
        "categories": categories,
    })

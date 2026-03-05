from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from ecommerce_app.models import Product, SuscriptorNewsletter
from cart.cart import Cart
from favorites.favorites import Favorites
from ecommerce_app.forms import FormularioNewsletter
import sib_api_v3_sdk
import stripe

# --- FUNCIONES AUXILIARES ---

def get_cart_products(request):
    cart_obj = Cart(request)
    return cart_obj.get_list_items()

def get_favorite_products(request):
    favorites_obj = Favorites(request)
    return favorites_obj.get_list_items()

def order_by_criteria(products):
    return sorted(products, key=lambda p: p.name)

def comes_from_checkout(request):
    status = request.GET.get('status')
    if status == 'success':
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
        messages.success(request, 'Payment made successfully!')
    elif status == 'cancel':
        messages.error(request, 'Payment has been cancelled')

# --- VISTAS ---

def home(request):
    comes_from_checkout(request)
    
    # Lógica específica para las "Popular Categories" con imagen
    category_names = Product.objects.values_list('category', flat=True).distinct()
    categories_data = []
    
    for cat_name in category_names:
        representative_product = Product.objects.filter(category=cat_name).order_by('id').first()
        if representative_product:
            categories_data.append({
                'name': cat_name,
                'image_url': representative_product.image.url
            })

    products = Product.objects.all()

    return render(request, 'home.html', {
        "categories_data": categories_data,
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
    })

def search(request):
    if request.method == "POST":
        referrer = request.META.get('HTTP_REFERER', '/')
        input_text = request.POST.get("input_text", "").strip()

        if not input_text:
            messages.error(request, "You have not searched for any product. Try writing something")
            return redirect(referrer)
        
        if len(input_text) > 40:
            messages.error(request, "Product name too long. Try a shorter one")
            return redirect(referrer)
        
        request.session["input_text"] = input_text
    
    input_text = request.session.get('input_text', '')
    products = Product.objects.filter(
        Q(name__icontains=input_text) | 
        Q(description__icontains=input_text) | 
        Q(category__icontains=input_text)
    )
    
    return render(request, "search.html", {
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
        "query": input_text,
    })

def filter_category(request, category):
    category = category.capitalize()
    referrer = request.META.get('HTTP_REFERER', '/')
    products = Product.objects.filter(category=category)

    if not products:
        messages.error(request, "The category you just searched for does not exist.")
        return redirect(referrer)
    
    return render(request, "filter.html", {
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
        "category": category,
    })

def detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        messages.error(request, "The product you are looking for does not exist.")
        return redirect('home')

    return render(request, 'detail.html', {
        "product": product,
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
    })

def cart(request):
    comes_from_checkout(request)
    cart_obj = Cart(request)
    cart_ids = get_cart_products(request)
    products = Product.objects.filter(id__in=cart_ids)

    if not products:
        messages.warning(request, "You don't have any products in your cart yet.")
        return redirect('home')

    return render(request, 'cart.html', {
        "products": order_by_criteria(products),
        "cart_products": cart_ids,
        "is_cart": True,
        "subtotal_dict": cart_obj.get_total_product(),
        "total": str(cart_obj.get_total_cart()),
    })

def favorites(request):
    fav_ids = get_favorite_products(request)
    products = Product.objects.filter(id__in=fav_ids)

    if not products:
        messages.warning(request, "You don't have any favorites yet.")
        return redirect('home')

    return render(request, 'favorites.html', {
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": fav_ids,
    })

def newsletter(request):
    referrer = request.META.get('HTTP_REFERER', '/')
    form = FormularioNewsletter(request.POST)
    if form.is_valid():
        email_destino = form.cleaned_data["email"]
        
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = settings.BREVO_API_KEY
        
        api_client = sib_api_v3_sdk.ApiClient(configuration)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
        
        html_content = render_to_string("newsletter_message.html", {})
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email_destino}],
            sender={"name": "Ragusa E-commerce", "email": "lautaroreche1@gmail.com"},
            subject="Thank you for subscribing",
            html_content=html_content,
        )
        
        try:
            api_instance.send_transac_email(send_smtp_email)
            messages.success(request, "Subscribed successfully!")
        except Exception:
            messages.error(request, "Error sending email.")
        
        return redirect(referrer)
        
    messages.error(request, "Invalid email.")
    return redirect(referrer)

@csrf_exempt
def checkout(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    if request.method == 'POST':
        try:
            total = int(float(request.POST.get('total'))) * 100 
        except (ValueError, TypeError):
            total = 100

        success_url = request.build_absolute_uri(reverse('home')) + '?status=success'
        cancel_url = request.build_absolute_uri(reverse('cart')) + '?status=cancel'

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Carrito de compra'},
                    'unit_amount': total,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return redirect(session.url, code=303)
    return redirect('home')

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from email.mime.text import MIMEText
from ecommerce.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_SENDER_NAME, BREVO_API_KEY
from ecommerce_app.models import Product, SuscriptorNewsletter
from cart.cart import Cart
from favorites.favorites import Favorites
from ecommerce_app.forms import FormularioNewsletter
import sib_api_v3_sdk
import stripe


CATEGORIES = Product.objects.values('category').distinct().order_by('category')

TRENDING_PRODUCTS = Product.objects.filter(is_trend=True)

TOP_OF_CATEGORY_PRODUCTS = Product.objects.filter(is_top_of_category=True)


def get_cart_products(request):
    cart_obj = Cart(request)
    cart_products = cart_obj.get_list_items()
    return cart_products

def get_favorite_products(request):
    favorites_obj = Favorites(request)
    favorite_products = favorites_obj.get_list_items()
    return favorite_products

def order_by_criteria(products):
    ordered_list = sorted(products, key=lambda p: p.name)
    return ordered_list



def home(request):
    # From checkout
    status = request.GET.get('status')
    if status == 'success':
        if 'cart' in request.session:
            del request.session['cart']
            request.session.modified = True
        messages.success(request, 'Payment made successfully!')
    elif status == 'cancel':
        messages.error(request, 'Payment has been cancelled')
    
    products = Product.objects.all()

    return render(request, 'home.html', {
        "categories": CATEGORIES,
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
        "trending_products": TRENDING_PRODUCTS,
        "top_of_category_products": TOP_OF_CATEGORY_PRODUCTS,
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
        
        products = Product.objects.filter(Q(name__icontains=input_text) | Q(description__icontains=input_text) | Q(category__icontains=input_text))
        if not products:
            messages.error(request, f'There is no product similar to "{input_text}". Try searching for the product in another way')
            return redirect(referrer)
        
        request.session["input_text"] = input_text
    
    input_text = request.session.get('input_text', '')
    products = Product.objects.filter(Q(name__icontains=input_text) | Q(description__icontains=input_text) | Q(category__icontains=input_text))
    
    return render(request, "search.html", {
        "categories": CATEGORIES,
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
        "trending_products": TRENDING_PRODUCTS,
        "top_of_category_products": TOP_OF_CATEGORY_PRODUCTS,
        "query": input_text,
    })


def filter_category(request, category):
    category = category.capitalize()
    referrer = request.META.get('HTTP_REFERER', '/')
    products = Product.objects.filter(category=category)

    if not products:
        messages.error(request, "The category you just searched for does not exist. Try selecting one of the existing categories")
        return redirect(referrer)
    
    return render(request, "filter.html", {
        "categories": CATEGORIES,
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
        "trending_products": TRENDING_PRODUCTS,
        "top_of_category_products": TOP_OF_CATEGORY_PRODUCTS,
        "category": category,
    })


def detail(request, product_id):
    referrer = request.META.get('HTTP_REFERER', '/')
    product = Product.objects.get(id=product_id)

    if not product:
        messages.error(request, "The product you are looking for does not exist. Try searching for the product in another way")
        return redirect(referrer)

    return render(request, 'detail.html', {
        "categories": CATEGORIES,
        "product": product,
        "cart_products": get_cart_products(request),
        "favorite_products": get_favorite_products(request),
        "trending_products": TRENDING_PRODUCTS,
        "top_of_category_products": TOP_OF_CATEGORY_PRODUCTS,
    })


def cart(request):
    cart_obj = Cart(request)
    cart_products = get_cart_products(request)
    products = Product.objects.filter(id__in=cart_products)

    if not products:
        messages.warning(request, "You do not have any products in your cart yet. Try adding a product")
        return redirect(home)

    return render(request, 'cart.html', {
        "categories": CATEGORIES,
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "trending_products": TRENDING_PRODUCTS,
        "top_of_category_products": TOP_OF_CATEGORY_PRODUCTS,
        "is_cart": True,
        "subtotal_dict": cart_obj.get_total_product(),
        "total": str(cart_obj.get_total_cart()),
    })


def favorites(request):
    favorite_products = get_favorite_products(request)
    products = Product.objects.filter(id__in=favorite_products)

    if not products:
        messages.warning(request, "You do not have any products selected as favorites yet. Try adding a product")
        return redirect(home)

    return render(request, 'favorites.html', {
        "categories": CATEGORIES,
        "products": order_by_criteria(products),
        "cart_products": get_cart_products(request),
        "trending_products": TRENDING_PRODUCTS,
        "top_of_category_products": TOP_OF_CATEGORY_PRODUCTS,
    })


def newsletter(request):
    referrer = request.META.get('HTTP_REFERER', '/')
    form = FormularioNewsletter(request.POST)
    if form.is_valid():
        email_destino = form.cleaned_data["email"]
        
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = BREVO_API_KEY
        
        api_client = sib_api_v3_sdk.ApiClient(configuration)
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(api_client)
        
        # Render the HTML content with context if necessary, or empty if not
        html_content = render_to_string("newsletter_message.html", {})
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email_destino}],
            sender={"name": "Ragusa E-commerce", "email": "lautaroreche1@gmail.com"},
            subject="Thank you for subscribing",
            html_content=html_content,
        )
        
        try:
            api_instance.send_transac_email(send_smtp_email)
            messages.success(request, "You have subscribed to our newsletter successfully. Soon you will receive a confirmation email")
        except Exception:
            messages.error(request, "Error sending email. Try again later")
        
        return redirect(referrer)
        
    messages.error(request, "The entered email is not valid. Try to enter a valid email")
    return redirect(referrer)


stripe.api_key = settings.STRIPE_SECRET_KEY
@csrf_exempt
def checkout(request):
    """
    Is possible to test the checkout with test cards numbers:
    https://docs.stripe.com/testing#international-cards
    """
    
    if request.method == 'POST':
        try:
            total = int(request.POST.get('total')) * 100 # EUR to cents
        except (ValueError, TypeError):
            total = 100  # Security fallback

        home_url = request.build_absolute_uri(reverse('home'))
        success_url = home_url + '?status=success'
        cancel_url = home_url + '?status=cancel'

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': 'Carrito de compra',
                    },
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

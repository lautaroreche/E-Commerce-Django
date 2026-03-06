from datetime import datetime
from .models import Product


def ecommerce_data(request):
    category_names = Product.objects.values_list('category', flat=True).distinct()
    categories_menu = []
    
    for cat_name in category_names:
        representative_product = Product.objects.filter(category=cat_name).first()
        if representative_product:
            categories_menu.append({
                'name': cat_name,
                'image_url': representative_product.image.url
            })

    return {
        'categories_menu': categories_menu,
        'all_categories': Product.objects.values('category').distinct().order_by('category'),
        'trending_products': Product.objects.filter(is_trend=True),
        'top_of_category_products': Product.objects.filter(is_top_of_category=True),
        'current_year': datetime.now().year
    }


def current_year(request):
    context = {
        'current_year': datetime.now().year
    }
    return context
    
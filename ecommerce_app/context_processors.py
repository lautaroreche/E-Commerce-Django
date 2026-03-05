from datetime import datetime
from .models import Product


def ecommerce_data(request):
    return {
        'all_categories': Product.objects.values('category').distinct().order_by('category'),
        'trending_products': Product.objects.filter(is_trend=True),
        'top_of_category_products': Product.objects.filter(is_top_of_category=True),
    }


def current_year(request):
    context = {
        'current_year': datetime.now().year
    }
    return context
    
"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from ecommerce_app.views import home, search, filter_category, cart, newsletter, favorites, checkout, detail
from cart.views import add_to_cart, remove_from_cart, decrement_from_cart
from favorites.views import manage_favorites, add_all_favorites_to_cart


# 1x1 transparent GIF used by the GitHub Pages landing to check that the server is awake
PING_GIF = b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"


def ping(request):
    response = HttpResponse(PING_GIF, content_type="image/gif")
    response["Cache-Control"] = "no-store"
    return response


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('filter_category/<str:category>/', filter_category, name='filter_category'),
    path('detail/<int:product_id>/', detail, name='detail'),
    path('cart/', cart, name='cart'),
    path('newsletter/', newsletter, name='newsletter'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('decrement_from_cart/<int:product_id>/', decrement_from_cart, name='decrement_from_cart'),
    path('favorites/', favorites, name='favorites'),
    path('manage_favorites/<int:product_id>/', manage_favorites, name='manage_favorites'),
    path('add_all_favorites_to_cart/', add_all_favorites_to_cart, name='add_all_favorites_to_cart'),
    path('checkout/', checkout, name='checkout'),
    path('ping.gif', ping, name='ping'),
]

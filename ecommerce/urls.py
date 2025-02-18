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
from ecommerce_app.views import home, search, filter, account, cart, newsletter, error, congrats, favorites
from cart.views import add_to_cart, remove_from_cart, decrement_product_from_cart, clear_cart
from favorites.views import add_to_favorites, remove_from_favorites


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name = 'home'),
    path('search/', search, name = 'search'),
    path('filter/<str:category>/', filter, name = 'filter'),
    path('account/', account, name = 'account'),
    path('cart/', cart, name = 'cart'),
    path('newsletter/', newsletter, name = 'newsletter'),
    path('error/', error, name = 'error'),
    path('congrats/', congrats, name = 'congrats'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name = 'remove_from_cart'),
    path('decrement_product_from_cart/<int:product_id>/', decrement_product_from_cart, name = 'decrement_product_from_cart'),
    path('clear_cart/', clear_cart, name = 'clear_cart'),
    path('favorites/', favorites, name = 'favorites'),
    path('add_to_favorites/<int:product_id>/', add_to_favorites, name = 'add_to_favorites'),
    path('remove_from_favorites/<int:product_id>/', remove_from_favorites, name = 'remove_from_favorites'),
]

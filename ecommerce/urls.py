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
from ecommerce_app.views import home, search, filter, cart, newsletter, favorites, feedback, custom_login, custom_logout, checkout, detail
from cart.views import add_to_cart, remove_from_cart, decrement_from_cart, clear_cart
from favorites.views import manage_favorites, clear_favorites, add_all_favorites_to_cart
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name = 'home'),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('home/', home, name = 'home'),
    path('search/', search, name = 'search'),
    path('filter/<str:category>/', filter, name = 'filter'),
    path('detail/<int:product_id>/', detail, name = 'detail'),
    path('cart/', cart, name = 'cart'),
    path('newsletter/', newsletter, name = 'newsletter'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name = 'add_to_cart'),
    path('remove_from_cart/<int:product_id>/', remove_from_cart, name = 'remove_from_cart'),
    path('decrement_from_cart/<int:product_id>/', decrement_from_cart, name = 'decrement_from_cart'),
    path('clear_cart/', clear_cart, name = 'clear_cart'),
    path('favorites/', favorites, name = 'favorites'),
    path('manage_favorites/<int:product_id>/', manage_favorites, name = 'manage_favorites'),
    path('clear_favorites/', clear_favorites, name = 'clear_favorites'),
    path('add_all_favorites_to_cart/', add_all_favorites_to_cart, name = 'add_all_favorites_to_cart'),
    path('feedback/', feedback, name = 'feedback'),
    path('checkout/', checkout, name = 'checkout'),
]

# Solo en desarrollo, para servir archivos de medios
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

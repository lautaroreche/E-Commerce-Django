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
from ecommerce_app.views import home, search, filter, account, cart, newsletter, error, congrats
from cart.views import add, remove, decrement, clear


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('search/', search, name='search'),
    path('filter/<str:category>/', filter, name='filter'),
    path('account/', account, name='account'),
    path('cart/', cart, name='cart'),
    path('newsletter/', newsletter, name='newsletter'),
    path('error/', error, name='error'),
    path('congrats/', congrats, name='congrats'),
    path('add/<int:product_id>/', add, name='add'),
    path('remove/<int:product_id>/', remove, name='remove'),
    path('decrement/<int:product_id>/', decrement, name='decrement'),
    path('clear/', clear, name='clear'),
]

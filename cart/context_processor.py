def has_cart(request):
    cart = request.session.get("cart", {})
    return bool(cart)

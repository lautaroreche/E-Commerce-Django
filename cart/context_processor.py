def has_cart(request):
    cart = request.session.get("cart", {})
    context = {
        "has_cart": bool(cart),
    }
    return context

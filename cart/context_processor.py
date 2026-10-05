def has_cart(request):
    cart = request.session.get("cart", {})
    context = {
        "has_cart": bool(cart),
        "cart_count": sum(item.get("quantity", 0) for item in cart.values()),
    }
    return context

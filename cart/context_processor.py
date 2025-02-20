def has_cart(request):
    cart = request.session.get("cart", {})
    return {"has_cart": bool(cart)}
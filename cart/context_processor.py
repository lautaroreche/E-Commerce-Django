def total_cart_amount(request):
    total=0
    if request.user.is_authenticated:
        cart = request.session.get("cart", {})
        for item in cart.values():
            total += int(float(item["price"]) * item["quantity"])
    print(total)
    return {"total_cart_amount": total}
class Cart():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart


    def add(self, product):
        print(product)
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "name": product.name,
                "price": str(product.price),
                "quantity": 1,
                "image": product.image.url,
            }
        else:
            for key, value in self.cart.items():
                if key == product_id:
                    value["quantity"] += 1
                    break
        self.save()


    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):
                if value["quantity"] > 1:
                    value["quantity"] -= 1
                else:
                    self.remove(product)
                break
        self.save()


    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True


    def get_total_product(self):
        subtotal = {}
        for key, value in self.cart.items():
            subtotal[key] = float(value["price"]) * value["quantity"]
        return subtotal


    def get_total_cart(self):
        total = 0
        for key, value in self.get_total_product().items():
            total += int(value)
        return total

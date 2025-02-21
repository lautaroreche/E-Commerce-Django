from ecommerce_app.models import Product


class Cart():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart


    def add(self, product_id):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 1,
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


    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    def decrement(self, product_id):
        product_id = str(product_id)
        for key, value in self.cart.items():
            if key == product_id:
                if value["quantity"] > 1:
                    value["quantity"] -= 1
                else:
                    self.remove(product_id)
                break
        self.save()


    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True


    def get_total_product(self):
        products = Product.objects.filter(id__in=self.cart.keys())
        subtotal = {}
        for key, value in self.cart.items():
            for product in products:
                if product.id == int(key):
                    subtotal[key] = float(product.price) * value["quantity"]
                    break
        return subtotal


    def get_total_cart(self):
        total = 0
        for key, value in self.cart.items():
            key = int(key)
            total += float(Product.objects.get(id=key).price) * value["quantity"]
        return total
    

    def get_list_items(self):
        return [int(key) for key in self.cart.keys()]

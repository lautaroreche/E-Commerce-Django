class Favorites():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        favorites = self.session.get("favorites")
        if not favorites:
            favorites = self.session["favorites"] = {}
        self.favorites = favorites


    def add(self, product):
        product_id = str(product.id)
        if product_id not in self.favorites:
            self.favorites[product_id] = {
                "name": product.name,
                "price": str(product.price),
                "image": product.image.url,
            }
        else:
            del self.favorites[product_id]
        self.save()


    def save(self):
        self.session["favorites"] = self.favorites
        self.session.modified = True


    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.favorites:
            del self.favorites[product_id]
            self.save()


    def clear(self):
        self.session["favorites"] = {}
        self.session.modified = True

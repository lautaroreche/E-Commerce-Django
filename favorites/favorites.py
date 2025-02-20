class Favorites():
    def __init__(self, request):
        self.request = request
        self.session = request.session
        favorites = self.session.get("favorites")
        if not favorites:
            favorites = self.session["favorites"] = []
        self.favorites = favorites


    def manage(self, product_id):
        if product_id not in self.favorites:
            self.favorites.append(product_id)
        else:
            self.favorites.remove(product_id)
        self.save()


    def save(self):
        self.session["favorites"] = self.favorites
        self.session.modified = True


    def clear(self):
        self.session["favorites"] = []
        self.session.modified = True

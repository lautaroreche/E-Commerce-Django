def has_favorites(request):
    favorites = request.session.get("favorites", [])
    return bool(favorites)

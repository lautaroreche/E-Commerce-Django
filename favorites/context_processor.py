def has_favorites(request):
    favorites = request.session.get("favorites", [])
    return {"has_favorites": bool(favorites)}

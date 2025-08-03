def has_favorites(request):
    favorites = request.session.get("favorites", [])
    context = {
        "has_favorites": bool(favorites),
    }
    return context

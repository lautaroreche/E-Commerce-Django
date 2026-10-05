def has_favorites(request):
    favorites = request.session.get("favorites", [])
    context = {
        "has_favorites": bool(favorites),
        "favorites_count": len(favorites),
    }
    return context

def has_favorites(request):
    flag = False
    if request.user.is_authenticated:
        favorites = request.session.get("favorites", {})
        if favorites != {}:
            flag = True
    return {"has_favorites": flag}

from datetime import datetime


def current_year(request):
    context = {
        'current_year': datetime.now().year
    }
    return context
    
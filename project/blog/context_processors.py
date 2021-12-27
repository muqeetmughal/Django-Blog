from . import models


def categories(request):

    categories = models.Category.objects.filter(level=0)

    return {
        "categories" : categories
    }
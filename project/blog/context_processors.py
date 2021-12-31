from . import models


def categories(request):

    categories = models.Category.objects.filter()

    return {
        "categories" : categories
    }
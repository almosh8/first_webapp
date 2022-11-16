from . import item_objects, category_objects, offer_objects


def item_exists(pk):
    return item_objects.filter(pk=pk).exists()
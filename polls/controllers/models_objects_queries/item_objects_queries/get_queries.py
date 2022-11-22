from django.core.exceptions import ObjectDoesNotExist

from . import item_objects, category_objects, offer_objects


def item_exists(pk):
    return item_objects.filter(pk=pk).exists()


def get_item(pk):
    try:
        return item_objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None

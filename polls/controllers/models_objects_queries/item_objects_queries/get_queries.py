from django.core.exceptions import ObjectDoesNotExist

from . import item_objects


def item_exists_in_db(pk):
    return item_objects.filter(pk=pk).exists()


def get_item_model(pk):
    try:
        return item_objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None


def get_child_items_model_list(parent_model):
    return list(item_objects.filter(parent_category=parent_model))


def get_root_items_model_list():
    return list(item_objects.filter(parent_category=None))

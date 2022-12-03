from polls.models.items.Category import Category
from polls.models.items.Offer import Offer


def item_price(item_model):
    if isinstance(item_model, Offer):
        return item_model.price
    elif isinstance(item_model, Category):
        return average_price(category=item_model)
    else:
        raise TypeError


def average_price(category):
    try:
        return category.sum_children // category.count_children
    except ZeroDivisionError:
        return 0
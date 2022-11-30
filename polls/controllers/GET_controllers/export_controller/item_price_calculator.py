from polls.models.items.Category import Category
from polls.models.items.Offer import Offer


def item_price(item):
    if isinstance(item, Offer):
        return item.price
    elif isinstance(item, Category):
        return average_price(category=item)
    else:
        raise TypeError


def average_price(category):
    try:
        return category.sum_children // category.count_children
    except ZeroDivisionError:
        return 0
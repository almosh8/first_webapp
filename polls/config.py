from enum import Enum

from polls.models.items.Category import Category
from polls.models.items.Item import Item
from polls.models.items.Offer import Offer


class ItemTypeString(Enum):
    CATEGORY = 'CATEGORY'
    OFFER = 'OFFER'

ItemTypeDict = {'CATEGORY': Category, 'OFFER': Offer, 'ITEM': Item}
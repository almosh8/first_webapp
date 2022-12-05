from enum import Enum

from polls.models.items.Category import Category
from polls.models.items.Item import Item
from polls.models.items.Offer import Offer


class ItemTypeString(Enum):
    CATEGORY = 'CATEGORY'
    OFFER = 'OFFER'

class ItemTypeClass(Enum):
    CATEGORY = Category
    OFFER = Offer
    ITEM = Item

item_type_class_dict = {
    ItemTypeString.CATEGORY.value: ItemTypeClass.CATEGORY.value,
    ItemTypeString.OFFER.value: ItemTypeClass.OFFER.value
}

class ItemDictKeys(Enum):
    TYPE = 'type'
    NAME = 'name'
    ID = 'id'
    PARENT_ID = 'parentId'
    PRICE = 'price'
    UPDATE_DATE = 'date'
    CHILDREN_LIST = 'children'
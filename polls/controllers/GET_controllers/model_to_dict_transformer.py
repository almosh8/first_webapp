from polls import config
from polls.config import ItemTypeString, ItemDictKeys
from polls.controllers.GET_controllers.item_price_calculator import item_price
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_item_model
from polls.models.items.Category import Category
from polls.models.items.Offer import Offer

def make_item_dict_from_model(item_model):
    item_dict = {}
    item_dict[ItemDictKeys.TYPE.value] = \
        ItemTypeString.OFFER.value if isinstance(item_model, config.item_type_class_dict[ItemTypeString.OFFER.value]) \
            else ItemTypeString.CATEGORY.value
    item_dict[ItemDictKeys.NAME.value] = item_model.name
    item_dict[ItemDictKeys.ID.value] = item_model.id
    item_dict[ItemDictKeys.PARENT_ID.value] = None if item_model.parent_category is None else item_model.parent_category.id
    item_dict[ItemDictKeys.PRICE.value] = item_price(item_model)
    item_dict[ItemDictKeys.UPDATE_DATE.value] = str(item_model.update_date.isoformat(timespec='milliseconds')).replace('+00:00', 'Z')
    return item_dict


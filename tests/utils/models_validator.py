from polls.models.items.Item import Item
from tests.utils.one_model_validator import ModelValidator


# to be inherited by TestCase class where asserts are implemented

class ModelsValidator(ModelValidator):
    def assert_items_added(self, import_items_dicts_list):
        for import_item_dict in import_items_dicts_list:
            saved_item_model = Item.objects.get(pk=import_item_dict['id'])
            self.assert_item_model_properties_match(import_item_dict, saved_item_model)

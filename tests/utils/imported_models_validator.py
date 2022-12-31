from polls.models.items.Item import Item
from tests.utils.model_properties_validator import ModelPropertiesValidator


# to be inherited by TestCase class where asserts are implemented

class ImportedModelsValidator(ModelPropertiesValidator):
    def assert_items_added(self, import_items_dicts_list):
        for import_item_dict in import_items_dicts_list:
            saved_item_model = Item.objects.get(pk=import_item_dict['id'])
            self.assert_item_model_properties_match(import_item_dict, saved_item_model)

from polls.config import ItemDictKeys
from polls.models.items.Item import Item

# to be inherited by TestCase class where asserts are implemented
class ModelValidator:
    def assert_items_added(self, import_items_dicts_list):
        for import_item_dict in import_items_dicts_list:
            saved_item_model = Item.objects.get(pk=import_item_dict['id'])
            self.assert_item_model_properties_match(import_item_dict, saved_item_model)

    def assert_item_model_properties_match(self, item_dict, item_model):
        self.assertIsInstance(item_model, self.import_item_class)
        self.assertEquals(item_dict[ItemDictKeys.ID.value], item_model.id)
        # self.assertEquals(item_dict[''], item_model.price)
        self.assertEquals(item_dict[ItemDictKeys.NAME.value], item_model.name)
        if item_model.parent_category is not None:
            self.assertEquals(item_dict[ItemDictKeys.PARENT_ID.value], item_model.parent_category.id)
        else:
            self.assertEquals(item_dict[ItemDictKeys.PARENT_ID.value], item_model.parent_category)
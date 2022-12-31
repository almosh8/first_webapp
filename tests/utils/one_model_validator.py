from polls.config import ItemDictKeys, item_type_class_dict

class ModelValidator:
    def assert_item_model_properties_match(self, item_dict, item_model):
        self.assertIsInstance(item_model, item_type_class_dict[item_dict[ItemDictKeys.TYPE.value]])
        self.assertEquals(item_dict[ItemDictKeys.ID.value], item_model.id)
        # self.assertEquals(item_dict[''], item_model.price)
        self.assertEquals(item_dict[ItemDictKeys.NAME.value], item_model.name)
        if item_model.parent_category is not None:
            self.assertEquals(item_dict[ItemDictKeys.PARENT_ID.value], item_model.parent_category.id)
        else:
            self.assertEquals(item_dict[ItemDictKeys.PARENT_ID.value], item_model.parent_category)
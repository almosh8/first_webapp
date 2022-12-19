from django.test import TestCase


from polls.config import ItemDictKeys, item_type_class_dict
from polls.controllers.DELETE_controllers.delete_controller.items_remover import remove_item_subtree
from polls.controllers.GET_controllers.export_controller.items_exporter import get_export_item_subtree_dict
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_item_model, \
    get_child_items_model_list
from polls.models.items.Item import Item
from tests import tests_config


class ItemsRemoverTest(TestCase):

    def setUp(self):
        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.parent_item_dict = tests_config.TEST_CATEGORY_DICT
        self.parent_item_id = self.parent_item_dict[ItemDictKeys.ID.value]
        self.child_item_dict = tests_config.TEST_OFFER_DICT
        self.child_item_id = self.child_item_dict[ItemDictKeys.ID.value]
        self.children_count = tests_config.TEST_CATEGORY_CHILDREN_COUNT

        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()

    def test_remove_child_item_subtree(self):
        remove_item_subtree(self.child_item_id)

        parent_item_model = get_item_model(self.parent_item_id)
        children_list = get_child_items_model_list(parent_item_model)
        self.assertEquals(len(children_list), self.children_count - 1)

        child_item_model = get_item_model(self.child_item_id)
        self.assertIs(child_item_model, None)

    def test_remove_parent_item_subtree(self):
        remove_item_subtree(self.parent_item_id)

        parent_item_model = get_item_model(self.parent_item_id)
        self.assertIs(parent_item_model, None)

        child_item_model = get_item_model(self.child_item_id)
        self.assertIs(child_item_model, None)

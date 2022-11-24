import json

from django.test import TestCase

from polls import config
from polls.controllers.import_controller import *
from tests import tests_config


class ItemsImporterTest(TestCase):

    def setUp(self):
        import_items_dict = tests_config.IMPORT_ITEMS_DICT
        import_items_dicts_list = import_items_dict['items']

        self.import_item_dict = import_items_dicts_list[0]
        self.import_item_class = config.ItemTypeDict[self.import_item_dict['type']]

        self.item_with_parent_absent = tests_config.TEST_OFFER_DICT
        self.item_with_parent_absent_class = config.ItemTypeDict[self.item_with_parent_absent['type']]


        self.items_importer = ItemsImporter(tests_config.IMPORT_ITEMS_DICT)
        self.item_importer = ItemsImporter.ItemImporter(self.import_item_dict)


    def test_items_import(self):
        self.items_importer.import_items()

        self.assert_item_model_added()

    def test_item_with_parent_absent_import(self):
        self.item_importer = ItemsImporter.ItemImporter(self.item_with_parent_absent)
        self.item_importer.import_item()

        saved_items_list = self.item_with_parent_absent_class.objects.filter(pk=self.item_with_parent_absent['id'])
        self.assertEquals(len(saved_items_list), 0)
        # items_to_add_after_parent_added
        pending_child_items_list = pending_items_manager.get_pending_children_list(self.item_with_parent_absent['parentId'])
        self.assertIn(self.item_with_parent_absent, pending_child_items_list)

    def test_make_and_save_item_model(self):
        self.item_importer.make_and_save_item_model()

        item_model = self.item_importer.item_model
        self.assertIsInstance(item_model, self.import_item_class)
        self.assert_item_model_properties_match(self.import_item_dict, item_model)

        self.assert_item_model_added()

    def assert_item_model_added(self):
        saved_item_model = self.import_item_class.objects.get(pk=self.import_item_dict['id'])
        self.assert_item_model_properties_match(self.import_item_dict, saved_item_model)

    def assert_item_model_properties_match(self, item_dict, item_model):
        self.assertIsInstance(item_model, self.import_item_class)
        self.assertEquals(item_dict['id'], item_model.id)
        # self.assertEquals(item_dict[''], item_model.price)
        self.assertEquals(item_dict['name'], item_model.name)
        if item_model.parent_category is not None:
            self.assertEquals(item_dict['parentId'], item_model.parent_category.id)
        else:
            self.assertEquals(item_dict['parentId'], item_model.parent_category)

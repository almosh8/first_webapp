from django.test import TestCase

from polls.config import ItemDictKeys, ItemTypeClass
from polls.controllers.POST_controllers.import_controller.items_importer import *
from tests import tests_config
from tests.utils.imported_models_validator import ImportedModelsValidator


class ItemsImporterTest(TestCase, ImportedModelsValidator):

    def setUp(self):
        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.expected_imported_items_dicts_list = tests_config.IMPORT_ITEMS_DICTS_LIST

        self.import_item_dict = tests_config.TEST_CATEGORY_DICT
        self.import_item_class = ItemTypeClass[self.import_item_dict[ItemDictKeys.TYPE.value]].value

        self.item_with_parent_absent = tests_config.TEST_OFFER_DICT


    def test_items_import(self):
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()

        self.assert_items_added(self.expected_imported_items_dicts_list)

    def test_reversed_items_import(self):
        reversed_import_items_batch = dict(tests_config.IMPORT_ITEMS_BATCH)
        reversed_import_items_batch['items'] = reversed_import_items_batch['items'][::-1]
        reversed_import_items_dicts_list = reversed_import_items_batch['items']

        items_importer = ItemsImporter(reversed_import_items_batch)
        items_importer.import_items()

        self.assert_items_added(reversed_import_items_dicts_list)

    def test_hande_item(self):
        items_importer = ItemsImporter(self.import_items_batch)
        parent_item = tests_config.TEST_CATEGORY_DICT
        child_item = tests_config.TEST_OFFER_DICT

        pending_items_manager.add_pending_item(parent_item['id'], child_item)
        items_importer.handle_item(parent_item)
        self.assert_items_added([parent_item, child_item])

    def test_item_with_parent_absent_import(self):
        self.item_importer = ItemsImporter.ItemImporter(self.item_with_parent_absent)
        self.item_importer.import_item()

        saved_items_list = self.import_item_class.objects.filter(pk=self.item_with_parent_absent['id'])
        self.assertEquals(len(saved_items_list), 0)
        # items_to_add_after_parent_added
        pending_child_items_list = pending_items_manager.get_pending_children(self.item_with_parent_absent['parentId'])
        self.assertIn(self.item_with_parent_absent, pending_child_items_list)

    def test_make_and_save_item_model(self):
        item_importer = ItemsImporter.ItemImporter(self.import_item_dict)
        item_importer.make_and_save_item_model()

        item_model = item_importer.item_model
        self.assertIsInstance(item_model, self.import_item_class)
        self.assert_item_model_properties_match(self.import_item_dict, item_model)

        self.assert_items_added([self.import_item_dict])

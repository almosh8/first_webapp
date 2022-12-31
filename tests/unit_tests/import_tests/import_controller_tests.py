from django.test import TestCase

from polls.config import ItemDictKeys, ItemTypeClass
from polls.controllers.POST_controllers.import_controller.items_importer import *
from tests import tests_config
from tests.unit_tests.import_tests.abstract_import_tests import AbstractItemsImporterTest
from tests.utils.imported_models_validator import ImportedModelsValidator


class ItemsImporterControllerTest(AbstractItemsImporterTest, TestCase, ImportedModelsValidator):
    import_item_dict = tests_config.TEST_CATEGORY_DICT
    import_item_class = ItemTypeClass[import_item_dict[ItemDictKeys.TYPE.value]].value

    item_with_parent_absent = tests_config.TEST_OFFER_DICT

    def import_items(self, import_items_batch):
        items_importer = ItemsImporter(import_items_batch)
        items_importer.import_items()

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

        pending_child_items_list = pending_items_manager.get_pending_children(self.item_with_parent_absent['parentId'])
        self.assertIn(self.item_with_parent_absent, pending_child_items_list)

    def test_make_and_save_item_model(self):
        item_importer = ItemsImporter.ItemImporter(self.import_item_dict)
        item_importer.make_and_save_item_model()

        self.assert_items_added([self.import_item_dict])

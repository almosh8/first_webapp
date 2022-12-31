from django.test import TestCase

from polls.config import ItemDictKeys, ItemTypeClass
from polls.controllers.POST_controllers.import_controller.items_importer import *
from tests import tests_config
from tests.utils.models_validator import ModelsValidator


class AbstractItemsImporterTest(TestCase, ModelsValidator):

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
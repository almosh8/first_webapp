from django.test import TestCase

from polls.config import ItemDictKeys, ItemTypeClass
from tests import tests_config
from tests.utils.imported_models_validator import ImportedModelsValidator

# to be inherited by concrete TestCase class where import_items and asserts are implemented

class AbstractItemsImporterTest(ImportedModelsValidator):
    import_items_batch = tests_config.IMPORT_ITEMS_BATCH
    expected_imported_items_dicts_list = tests_config.IMPORT_ITEMS_DICTS_LIST

    def test_items_import(self):
        self.import_items(self.import_items_batch)

        self.assert_items_added(self.expected_imported_items_dicts_list)

    def test_reversed_items_import(self):
        reversed_import_items_batch = dict(tests_config.IMPORT_ITEMS_BATCH)
        reversed_import_items_batch['items'] = reversed_import_items_batch['items'][::-1]
        reversed_import_items_dicts_list = reversed_import_items_batch['items']

        self.import_items(reversed_import_items_batch)

        self.assert_items_added(reversed_import_items_dicts_list)
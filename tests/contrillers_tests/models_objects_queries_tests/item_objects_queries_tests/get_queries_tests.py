from django.test import TestCase

from polls.config import ItemDictKeys
from polls.controllers.POST_controllers.import_controller import ItemsImporter
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import *
from polls.models.items.Category import Category
from tests import tests_config, ModelValidator


class ItemsImporterTest(TestCase, ModelValidator):

    EXTRA_CHARACTER = '#'

    def setUp(self):
        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.import_items_dicts_list = tests_config.IMPORT_ITEMS_DICTS_LIST

        self.existing_category_dict = tests_config.TEST_CATEGORY_DICT
        self.existing_offer_dict = tests_config.TEST_OFFER_DICT
        self.existing_item_id = self.existing_category_dict[ItemDictKeys.ID.value]
        self.absent_item_id = self.existing_item_id + self.EXTRA_CHARACTER
        # there is one category in batch and all other items are its children
        self.children_count = len(self.import_items_dicts_list) - 1

        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()

    def test_item_exists_in_db(self):
        result_with_existing_item = item_exists_in_db(self.existing_item_id)
        result_with_absent_item = item_exists_in_db(self.absent_item_id)

        self.assertTrue(result_with_existing_item)
        self.assertFalse(result_with_absent_item)

    def test_get_item_model(self):
        result_with_existing_item = get_item_model(self.existing_item_id)
        result_with_absent_item = get_item_model(self.absent_item_id)

        self.assertIsInstance(result_with_existing_item, Category)
        self.assert_item_model_properties_match(self.existing_category_dict, result_with_existing_item)
        self.assertIs(result_with_absent_item, None)

    def test_get_child_items_model_list(self):
        parent_category_model = get_item_model(self.existing_category_dict[ItemDictKeys.ID.value])
        child_offer_model = get_item_model(self.existing_offer_dict[ItemDictKeys.ID.value])

        result_with_existing_children = get_child_items_model_list(parent_category_model)
        result_with_absent_children = get_child_items_model_list(child_offer_model)

        self.assertEquals(len(result_with_existing_children), self.children_count)
        self.assertEquals(len(result_with_absent_children), 0)


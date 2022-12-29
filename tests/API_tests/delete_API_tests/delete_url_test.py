import json

from django.test import TestCase
from rest_framework.test import RequestsClient

from polls.config import ItemDictKeys
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_item_model, \
    get_child_items_model_list
from tests import tests_config


class DeleteUrlTest(TestCase):

    def setUp(self):
        self.client = RequestsClient()

        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.parent_item_dict = tests_config.TEST_CATEGORY_DICT
        self.parent_item_id = self.parent_item_dict[ItemDictKeys.ID.value]
        self.child_item_dict = tests_config.TEST_OFFER_DICT
        self.child_item_id = self.child_item_dict[ItemDictKeys.ID.value]
        self.children_count = tests_config.TEST_CATEGORY_CHILDREN_COUNT

        self.prefix_url = 'http://testserver'
        self.get_url = '/delete/'
        self.delete_parent_url = self.prefix_url + self.get_url + str(self.parent_item_id)
        self.delete_child_url = self.prefix_url + self.get_url + str(self.child_item_id)

        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()

    def test_remove_child_item_subtree_request(self):
        response = self.client.delete(self.delete_child_url)
        self.assertEquals(response.status_code, 200)

        parent_item_model = get_item_model(self.parent_item_id)
        children_list = get_child_items_model_list(parent_item_model)
        self.assertEquals(len(children_list), self.children_count - 1)

        child_item_model = get_item_model(self.child_item_id)
        self.assertIs(child_item_model, None)

    def test_remove_parent_item_subtree_request(self):
        response = self.client.delete(self.delete_parent_url)
        self.assertEquals(response.status_code, 200)

        parent_item_model = get_item_model(self.parent_item_id)
        self.assertIs(parent_item_model, None)

        child_item_model = get_item_model(self.child_item_id)
        self.assertIs(child_item_model, None)

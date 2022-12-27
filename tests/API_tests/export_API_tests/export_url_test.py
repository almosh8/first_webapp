import json

from django.test import TestCase
from rest_framework.test import RequestsClient

from polls.config import ItemDictKeys
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from tests import tests_config


class GetUrlTest(TestCase):

    def setUp(self):
        self.client = RequestsClient()

        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.expected_subtree_dict = tests_config.TEST_SUBTREE
        self.root_item_dict = tests_config.IMPORT_ITEMS_DICTS_LIST[0]
        self.root_item_id = self.root_item_dict[ItemDictKeys.ID.value]

        self.prefix_url = 'http://testserver'
        self.get_url = '/nodes/'
        self.get_root_url = self.prefix_url + self.get_url + str(self.root_item_id)

        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()





    def test_export_request(self):
        response = self.client.get(self.get_root_url)
        response_content = response.content.decode()
        response_content = json.loads(response_content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_content, self.expected_subtree_dict)
import json

from django.test import TestCase
from rest_framework.test import RequestsClient

from polls.config import ItemDictKeys
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from tests import tests_config
from tests.utils.models_validator import ModelsValidator


class PostUrlTest(TestCase, ModelsValidator):

    def setUp(self):
        self.client = RequestsClient()
        self.prefix_url = 'http://testserver'
        self.post_url = '/imports'
        self.post_full_url = self.prefix_url + self.post_url

        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.expected_imported_items_dicts_list = tests_config.IMPORT_ITEMS_DICTS_LIST



    def test_export_request(self):
        response = self.client.post(self.post_full_url, json=self.import_items_batch)
        self.assertEquals(response.status_code, 200)

        self.assert_items_added(self.expected_imported_items_dicts_list)
import json

from rest_framework.test import APITestCase
from tests.unit_tests.export_tests.abstract_export_tests import AbstractItemsExporterTest


class ItemsExporterAPITests(AbstractItemsExporterTest, APITestCase):
    prefix_url = 'http://testserver'
    get_url = '/nodes/'

    def get_export_item_subtree_dict(self, item_id):
        get_root_url = self.prefix_url + self.get_url + str(item_id)
        response = self.client.get(get_root_url)
        response_content = response.content.decode()
        response_content = json.loads(response_content)

        self.assertEquals(response.status_code, 200)
        return response_content

from rest_framework.test import APITestCase

from tests.unit_tests.import_tests.abstract_import_tests import AbstractItemsImporterTest


class ItemsImporterAPITests(AbstractItemsImporterTest, APITestCase):
    prefix_url = 'http://testserver'
    get_url = '/imports'

    def import_items(self, import_items_batch):
        import_items_url = self.prefix_url + self.get_url
        response = self.client.post(import_items_url, import_items_batch, format='json')
        self.assertEquals(response.status_code, 200)

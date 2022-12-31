from rest_framework.test import APITestCase
from tests.unit_tests.delete_tests.abstract_delete_tests import AbstractItemsRemoverTests


class ItemsRemoverAPITests(AbstractItemsRemoverTests, APITestCase):

    prefix_url = 'http://testserver'
    get_url = '/delete/'

    def remove_item_subtree(self, item_id):
        delete_root_url = self.prefix_url + self.get_url + str(item_id)
        response = self.client.delete(delete_root_url)
        self.assertEquals(response.status_code, 200)


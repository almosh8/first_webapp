from django.test import TestCase

import polls.controllers.DELETE_controllers.delete_controller.items_remover as delete_controller
from tests.unit_tests.delete_tests.abstract_delete_tests import AbstractItemsRemoverTests


class ItemsRemoverControllerTests(AbstractItemsRemoverTests, TestCase):

    def remove_item_subtree(self, item_id):
        delete_controller.remove_item_subtree(item_id)

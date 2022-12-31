from django.test import TestCase

import polls.controllers.GET_controllers.export_controller.items_exporter as export_controller
from tests.unit_tests.export_tests.abstract_export_tests import AbstractItemsExporterTest


class ItemsExporterControllerTests(AbstractItemsExporterTest, TestCase):

    def get_export_item_subtree_dict(self, item_id):
        return export_controller.get_export_item_subtree_dict(item_id)

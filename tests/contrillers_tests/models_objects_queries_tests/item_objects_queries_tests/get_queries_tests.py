from django.test import TestCase

from polls.controllers.POST_controllers.import_controller import ItemsImporter
from tests import tests_config


class ItemsImporterTest(TestCase):

    def setUp(self):
        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(tests_config.IMPORT_ITEMS_DICT)
        items_importer.import_items()


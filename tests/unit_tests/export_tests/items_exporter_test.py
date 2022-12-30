from django.test import TestCase


from polls.config import ItemDictKeys, item_type_class_dict
from polls.controllers.GET_controllers.export_controller.items_exporter import get_export_item_subtree_dict
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from polls.models.items.Item import Item
from tests import tests_config


class ItemsExporterTest(TestCase):

    def setUp(self):
        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.export_items_subtree_dict = tests_config.EXPORT_ITEMS_SUBTREE_DICT
        self.root_item_dict = tests_config.IMPORT_ITEMS_DICTS_LIST[0]
        self.root_item_id = self.root_item_dict[ItemDictKeys.ID.value]

        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()

    def test_get_item_subtree_dict(self):
        result_subtree_dict = get_export_item_subtree_dict(self.root_item_id)

        self.assertEquals(result_subtree_dict, self.export_items_subtree_dict)
from polls.config import ItemDictKeys
from polls.controllers.POST_controllers.import_controller.items_importer import ItemsImporter
from tests import tests_config


# to be inherited by concrete TestCase class where get_export_item_subtree_dict and asserts are implemented

class AbstractItemsExporterTest():

    def setUp(self):
        self.import_items_batch = tests_config.IMPORT_ITEMS_BATCH
        self.export_items_subtree_dict = tests_config.EXPORT_ITEMS_SUBTREE_DICT
        self.root_item_dict = tests_config.IMPORT_ITEMS_DICTS_LIST[0]
        self.root_item_id = self.root_item_dict[ItemDictKeys.ID.value]

        # assume ItemsImporter is already tested and works correctly
        items_importer = ItemsImporter(self.import_items_batch)
        items_importer.import_items()

    def test_get_item_subtree_dict(self):
        result_subtree_dict = self.get_export_item_subtree_dict(self.root_item_id)

        self.assertEquals(result_subtree_dict, self.export_items_subtree_dict)
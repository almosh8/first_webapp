import json

from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from polls import config
from polls.controllers.import_controller.parent_category_updater import *
from polls.models import Category, Offer
from polls.controllers.import_controller.items_importer import *
from tests import tests_config


class ItemsImporterTest(TestCase):



    def setUp(self):
        import_items_dict = tests_config.IMPORT_ITEMS_DICT
        import_items_dicts_list = import_items_dict['items']
        self.import_category_dict = import_items_dicts_list[0]
        self.items_importer = ItemsImporter(tests_config.IMPORT_ITEMS_DICT)
        self.item_importer = ItemsImporter.ItemImporter(self.import_category_dict)

    def test_items_import(self):
        self.items_importer.import_items()

    def test_make_item_model(self):
        self.item_importer.make_item_model()

        item_model = self.item_importer.item_model
        self.assertIsInstance(item_model, config.ItemTypeDict[self.import_category_dict['type']])
        self.assert_item_model_properties(self.import_category_dict, item_model)

    def assert_item_model_properties(self, item_dict, item_model):
        self.assertEquals(item_dict['id'], item_model.id)
        # self.assertEquals(item_dict[''], item_model.price)
        self.assertEquals(item_dict['name'], item_model.name)
        if item_model.parent_category is not None:
            self.assertEquals(item_dict['parentId'], item_model.parent_category.id)
        else:
            self.assertEquals(item_dict['parentId'], item_model.parent_category)



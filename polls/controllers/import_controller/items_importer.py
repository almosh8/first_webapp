from dateutil.parser import isoparse

from polls.config import ItemTypeString
from polls.controllers.import_controller import ChildRemover, ChildAdder, pending_items_manager
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import item_exists, get_item
from polls.models.items.Category import Category
from polls.models.items.Offer import Offer


class ItemsImporter:


    def __init__(self, batch: dict):
        self.items = batch['items']

        pending_items_manager.forget_all()
        global update_date
        update_date = batch['updateDate']

    def import_items(self):
        for item in self.items:
            item_importer = self.ItemImporter(item)
            item_importer.import_item()

    class ItemImporter:

        def __init__(self, item: dict):
            self.item = item
            self.parent_item_id = item['parentId']
            self.item_type = item['type']
            self.item_model = None


        def import_item(self):
            if self.must_add_parent_first():
                self.remember_item_waiting_for_parent()
            else:
                self.make_and_save_item_model()

        def must_add_parent_first(self):
            return (self.parent_item_id is not None) and (not item_exists(pk=self.parent_item_id))

        def remember_item_waiting_for_parent(self):
            pending_items_manager.add_pending_item(self.parent_item_id, self.item)

        def make_and_save_item_model(self):
            self.make_item_model()
            self.save_item_model()

        def make_item_model(self):
            if self.item_type == ItemTypeString.OFFER.value:
                self.item_model = Offer()
                self.set_specific_offer_model_properties()
            elif self.item_type == ItemTypeString.CATEGORY.value:
                self.item_model = Category()
                self.set_specific_category_model_properties()
            else:
                raise ValueError
            self.set_unspecific_item_model_properties()

        def set_specific_offer_model_properties(self):
            self.item_model.price = self.item['price']

        def set_specific_category_model_properties(self):
            existing_category_model = get_item(self.item['id'])
            if existing_category_model is not None:
                self.item_model.sum_children = existing_category_model.sum_children
                self.item_model.count_children = existing_category_model.count_children

        def set_unspecific_item_model_properties(self):

            self.item_model.name = self.item['name']
            self.item_model.id = self.item['id']
            if self.parent_item_id is not None:
                self.item_model.parent_category = get_item(self.parent_item_id)
            global update_date
            self.item_model.update_date = isoparse(update_date)

        def save_item_model(self):
            self.update_existing_variant_parents()
            self.update_new_variant_parents()
            self.item_model.save()

        def update_existing_variant_parents(self):
            existing_item_model = get_item(self.item_model.id)
            if existing_item_model is not None:
                item_remover = ChildRemover(existing_item_model)
                item_remover.update_parents()

        def update_new_variant_parents(self):
            item_adder = ChildAdder(self.item_model)
            item_adder.update_parents()
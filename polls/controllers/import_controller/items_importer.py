from dateutil.parser import isoparse

from polls.config import ItemTypeString
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import item_exists, get_item
from polls.models.items.Category import Category
from polls.models.items.Offer import Offer

items_to_add_after_parent_added = None

class ItemsImporter:


    def __init__(self, batch: dict):
        self.items = batch['items']

        global items_to_add_after_parent_added
        items_to_add_after_parent_added = {}
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
            global items_to_add_after_parent_added
            if self.parent_item_id not in items_to_add_after_parent_added:
                items_to_add_after_parent_added[self.parent_item_id] = []
            items_to_add_after_parent_added[self.parent_item_id].append(self.item)

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




    def set_item_properties(self, item_dict):

        type = item_dict['type']
        parent_id = item_dict['parentId']
        if type == ItemTypeString.OFFER.value:
            item = Offer(pk=item_dict['id'])
            item.price = item_dict['price']
        elif type == ItemTypeString.CATEGORY.value:
            try:  # save current parent_category info
                item = Category.objects.get(pk=item_dict['id'])
            except ObjectDoesNotExist:  # add new parent_category
                item = Category(pk=item_dict['id'])
        else:
            raise ValueError

        item.name = item_dict['name']
        item.pk = item_dict['id']
        if parent_id is not None:
            item.parent_category = Category.objects.get(pk=parent_id)
        item.update_date = isoparse(update_date)
        print(f'item saved {item_dict}')
        item.commit()

        if item.pk in children:  # children not added yet
            for child in children[item.pk]:
                add_item(child)
            children[item.pk].clear()

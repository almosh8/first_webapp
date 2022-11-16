from polls.config import ItemType
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import item_exists
from polls.models.items.Category import Category


class ItemsImporter:

    items_to_add_after_parent_added = None

    def __init__(self, batch: dict):
        self.update_date = batch['updateDate']
        self.items = batch['items']

    def add_items(self):
        for item in self.items:
            self.add_item(item)

    class ItemImporter:

        def __init__(self, item: dict):
            self.item = item
            self.parent_item_id = item['parentId']


        def add_item(self):
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


    def set_item_properties(self, item_dict):

        type = item_dict['type']
        parent_id = item_dict['parentId']
        if type == ItemType.OFFER.value:
            item = Offer(pk=item_dict['id'])
            item.price = item_dict['price']
        elif type == ItemType.CATEGORY.value:
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

from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_item_model
from polls.controllers.parent_category_updater import ChildRemover


def remove_item_subtree(item_id):
    item = get_item_model(item_id)

    parent_updater = ChildRemover(item)
    parent_updater.update_parents()

    item.delete()
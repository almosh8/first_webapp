items_to_add_after_parent_added = {}

def forget_all():
    items_to_add_after_parent_added.clear()

def add_pending_item(parent_item_id, item_dict):
    if not parent_item_id in items_to_add_after_parent_added:
        items_to_add_after_parent_added[parent_item_id] = []
    items_to_add_after_parent_added[parent_item_id].append(item_dict)

def get_pending_children_list(parent_id) -> list:
    if parent_id in items_to_add_after_parent_added:
        return items_to_add_after_parent_added[parent_id]
    return []
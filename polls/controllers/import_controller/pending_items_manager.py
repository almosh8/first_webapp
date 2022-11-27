from collections import deque

items_to_add_after_parent_added = {}

def clear_children(parent_id):
    items_to_add_after_parent_added[parent_id].clear()

def clear_all():
    items_to_add_after_parent_added.clear()

def add_pending_item(parent_item_id, item_dict):
    if not parent_item_id in items_to_add_after_parent_added:
        items_to_add_after_parent_added[parent_item_id] = deque()
    items_to_add_after_parent_added[parent_item_id].append(item_dict)

def get_pending_children(parent_id):
    if parent_id in items_to_add_after_parent_added:
        while len(items_to_add_after_parent_added[parent_id]) > 0:
            yield items_to_add_after_parent_added[parent_id].pop()
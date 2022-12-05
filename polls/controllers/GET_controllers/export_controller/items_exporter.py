from polls.config import ItemDictKeys
from polls.controllers.GET_controllers.model_to_dict_transformer import make_item_dict_from_model
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_item_model, get_child_items_model_list


def __init__(self, root_item_id):
    self.root_item_model = get_item_model(root_item_id)
    self.subtree_dict = make_item_dict_from_model(self.root_item_model)

def export_item_subtree_dict(root_item_id):
    item_model = get_item_model(root_item_id)
    return get_item_subtree_dict(item_model)

def get_item_subtree_dict(item_model):

    item_dict = make_item_dict_from_model(item_model)
    add_children_to_item_dict(item_model, item_dict)

    return item_dict


def add_children_to_item_dict(item_model, item_dict):
    child_items_dict_list = get_child_items_dict_list(item_model)
    item_dict[ItemDictKeys.CHILDREN_LIST.value] = child_items_dict_list


def get_child_items_dict_list(item_model):
    children = []
    children_model_list = get_child_items_model_list(item_model)
    for child_model in children_model_list:
        children.append(get_item_subtree_dict(child_model))
    if len(children) == 0:
        return None
    return children

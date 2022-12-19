from polls.config import ItemDictKeys
from polls.controllers.GET_controllers.model_to_dict_transformer import make_item_dict_from_model
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_child_items_model_list


class ConditionalItemSubtreeExporter:

    # specify item_validator if you want to export only specific items matching certain condition
    def __init__(self, root_item_model, item_validator=lambda x: True):
        self.root_item_model = root_item_model
        self.validate_item = item_validator

    def export_item_subtree_dict(self):
        return self.__get_item_subtree_dict(self.root_item_model)

    def __get_item_subtree_dict(self, item_model):
        if not self.validate_item(item_model):
            return None

        item_dict = make_item_dict_from_model(item_model)
        self.__add_children_to_item_dict(item_model, item_dict)

        return item_dict

    def __add_children_to_item_dict(self, item_model, item_dict):
        child_items_dict_list = self.__get_child_items_dict_list(item_model)
        item_dict[ItemDictKeys.CHILDREN_LIST.value] = child_items_dict_list

    def __get_child_items_dict_list(self, item_model):
        children = []
        children_model_list = get_child_items_model_list(item_model)
        for child_model in children_model_list:
            children.append(self.__get_item_subtree_dict(child_model))  # include children dicts recursively
        if len(children) == 0:
            return None
        return children

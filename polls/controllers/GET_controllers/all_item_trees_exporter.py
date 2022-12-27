from polls.controllers.GET_controllers.items_subtree_exporter import ConditionalItemSubtreeExporter
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_root_items_model_list


def export_all_item_trees_with_condition(items_filter=lambda x: True):
    all_root_items_model_list = get_root_items_model_list()
    all_root_items_dict_list = []
    for root_item_model in all_root_items_model_list:
        root_subtree_exporter = ConditionalItemSubtreeExporter(root_item_model, items_filter)
        root_item_dict = root_subtree_exporter.export_item_subtree_dict()
        all_root_items_dict_list.append(root_item_dict)
    return all_root_items_dict_list

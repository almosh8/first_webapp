from polls.config import ItemDictKeys
from polls.controllers.GET_controllers.items_subtree_exporter import ConditionalItemSubtreeExporter
from polls.controllers.GET_controllers.model_to_dict_transformer import make_item_dict_from_model
from polls.controllers.models_objects_queries.item_objects_queries.get_queries import get_item_model, \
    get_child_items_model_list


def get_export_item_subtree_dict(root_item_id):
    item_model = get_item_model(root_item_id)
    item_subtree_exporter = ConditionalItemSubtreeExporter(item_model)
    item_subtree_dict = item_subtree_exporter.export_item_subtree_dict()
    return item_subtree_dict

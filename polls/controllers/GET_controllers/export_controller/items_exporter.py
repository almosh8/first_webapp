from polls.controllers.models_objects_queries.item_objects_queries.get_queries import item_exists_in_db, get_item_model

class ItemsExporter:

    def __init__(self, parent_item_id):
        self.parent_item_model = get_item_model(parent_item_id)

    def get_dict(self, item=None):
        if item is None:
            item = self.item
        print(f'getting dict for {item.name}')

        dict = {}
        dict['type'] = OFFER if isinstance(item, Offer) else CATEGORY
        dict['name'] = item.name
        dict['id'] = item.id
        dict['url'] = item.url
        dict['parentId'] = None if item.parent_category is None else item.parent_category.id
        dict['price'] = item.price if isinstance(item, Offer) else item.average_price()
        dict['date'] = str(item.update_date.isoformat(timespec='milliseconds')).replace('+00:00', 'Z')
        if self.include_children:
            dict['children'] = None if isinstance(item, Offer) else self.get_children(item)

        return dict

    class ItemSerializer:
        # item is Offer or Category instance

        def get_children(self, item):
            children = []
            children_list = item.get_children()
            print(item.name, children_list)
            for child in children_list:
                children.append(self.get_dict(child))
            return children



        def __init__(self, item, include_children=True):
            self.include_children = include_children
            self.item = item

        def get_json(self, dict=None):
            if dict is None:
                dict = self.get_dict()
            # print(dict['children'])
            return json.dumps(dict, ensure_ascii=False).encode('utf8')
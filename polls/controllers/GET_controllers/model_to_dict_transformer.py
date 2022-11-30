class ModelToDictTransformer:

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
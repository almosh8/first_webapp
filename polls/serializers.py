import ast
import json

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from polls.models import Offer

CATEGORY = 'CATEGORY'
OFFER = 'OFFER'


class Item:
    def __init__(self, item):
        self.type = dict['type']
        self.name = dict['name']
        self.id = dict['id']
        self.price = dict['price']
        self.children = dict['children']
        self.update_date = dict['updateDate']
        self.parent_id = dict['ParentId']


class MyDeserializer:

    def __init__(self, json_data):
        self.json_data = json_data

    def get_dict(self):
        return json.loads(self.json_data)

class MySerializer:

    def __init__(self, dict_data):
        self.dict_data = dict_data

    def get_json(self):
        return json.dumps(self.dict_data)


class ItemSerializer:
    # item is Offer or Category instance

    def get_children(self, item):
        children = []
        children_list = item.get_children()
        print(item.name, children_list)
        for child in children_list:
            children.append(self.get_dict(child))
        return children

    def get_dict(self, item=None):
        if item is None:
            item = self.item
        print(f'getting dict for {item.name}')

        dict = {}
        dict['type'] = OFFER if isinstance(item, Offer) else CATEGORY
        dict['name'] = item.name
        dict['id'] = item.id
        dict['parentId'] = None if item.parent_category is None else item.parent_category.id
        dict['price'] = item.price if isinstance(item, Offer) else item.average_price()
        dict['date'] = str(item.update_date.isoformat(timespec='milliseconds')).replace('+00:00', 'Z')
        if self.include_children:
            dict['children'] = None if isinstance(item, Offer) else self.get_children(item)

        return dict

    def __init__(self, item, include_children = True):
        self.include_children = include_children
        self.item = item

    def get_json(self, dict=None):
        if dict is None:
            dict = self.get_dict()
        #print(dict['children'])
        return json.dumps(dict, ensure_ascii=False).encode('utf8')

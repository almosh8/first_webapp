import ast
import json

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from polls.models import Offer

CATEGORY = 'FOLDER'
OFFER = 'FILE'


class Item:
    def __init__(self, item):
        self.type = dict['type']
        self.name = dict['name']
        self.id = dict['id']
        self.price = dict['price']
        self.children = dict['children']
        self.update_date = dict['updateDate']
        self.parent_id = dict['ParentId']
        self.url = dict['url']


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




import json

from django.test import TestCase
from django.utils.datetime_safe import datetime
from rest_framework import request
from rest_framework.parsers import JSONParser

from .models import Category, Offer
from .serializers import ItemSerializer, MyDeserializer
from .views import add_items


def get_offer(id):
    return Offer(pk=id, name='test', price=1, update_date=datetime.now())


class CategoryModelTest(TestCase):

    def test_category_average_price(self):
        category = Category(sum_children=1)

        category.sum_children += 5
        assert category.sum_children == 6

        category.count_children += 2
        assert category.count_children == 2

        avg = category.average_price()
        self.assertIs(avg, 3)

    def test_category_add_child(self):
        category = Category()
        child_offer = Offer(price=15)
        category.add_child(child_offer)
        self.assertIs(category.average_price(), 15)
        child_category = Category(sum_children=8, count_children=2)
        category.add_child(child_category)
        self.assertIs(category.average_price(), 7)


class SerializersTest(TestCase):
    big_json = '[{"items": [{"type": "CATEGORY","name": "Товары","id": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1","parentId": None}],"updateDate": "2022-02-01T12:00:00.000Z"},{"items": [{"type": "CATEGORY","name": "Смартфоны","id": "d515e43f-f3f6-4471-bb77-6b455017a2d2","parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"},{"type": "OFFER","name": "jPhone 13","id": "863e1a7a-1304-42ae-943b-179184c077e3","parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2","price": 79999},{"type": "OFFER","name": "Xomiа Readme 10","id": "b1d8fd7d-2ae3-47d5-b2f9-0f094af800d4","parentId": "d515e43f-f3f6-4471-bb77-6b455017a2d2","price": 59999}],"updateDate": "2022-02-02T12:00:00.000Z"},{"items": [{"type": "CATEGORY","name": "Телевизоры","id": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2","parentId": "069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"},{"type": "OFFER","name": "Samson 70\" LED UHD Smart","id": "98883e8f-0507-482f-bce2-2fb306cf6483","parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2","price": 32999},{"type": "OFFER","name": "Phyllis 50\" LED UHD Smarter","id": "74b81fda-9cdc-4b63-8927-c978afed5cf4","parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2","price": 49999}],"updateDate": "2022-02-03T12:00:00.000Z"},{"items": [{"type": "OFFER","name": "Goldstar 65\" LED UHD LOL Very Smart","id": "73bc3b36-02d1-4245-ab35-3106c9ee1c65","parentId": "1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2","price": 69999}],"updateDate": "2022-02-03T15:00:00.000Z"}]'
    json_data = '{"name": "Товары", "b": None}'
    data = {'name': 'Товары', 'b': None}

    def test_serialize(self):
        data = self.data
        serializer = ItemSerializer(data)
        json_data = serializer.get_json()
        self.assertEquals(json_data, self.json_data)

    def test_deserialize(self):
        json_data = self.json_data
        deserializer = MyDeserializer(json_data)
        data = deserializer.get_dict()
        self.assertEquals(data, self.data)


class AddItemTest(TestCase):
    dict_item = {'type': 'CATEGORY', 'name': 'Смартфоны', 'id': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                 'parentId': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'}

    def test_add_offer(self):
        root = Category(id='test_root')
        root.save()
        parent = Category(id='test_parent', parent_category=root)
        parent.save()
        child = Offer(id='test_child', parent_category=parent, price=1)
        child.save()
        self.assertIs(root.average_price() == 1)


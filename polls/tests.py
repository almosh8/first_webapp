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





import random
from django.test import TestCase
from polls.controllers.export_controller import *
from polls.models import Offer, Category

class TestExport(TestCase):

    def setUp(self):
        self.offer = Offer(pk = 'test')
        self.category = Category(pk = 'test')

    def test_offer_price(self):
        self.offer.price = 10

        self.assertEquals(item_price(self.offer), 10)
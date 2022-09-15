import json

from django.test import TestCase
from django.utils.datetime_safe import datetime
import polls.controllers.import_controller
from polls.models import Category, Offer


class CategoryUpdaterTest(TestCase):

    def setUp(self):
        self.category_updater = CategoryUpdaterTest()
        self.category = Category(sum_children=11, count_children=3)
        self.child = Offer(price=4)

    def test_child_removed(self):
        self.category_updater.child_removed(self.category, self.child)
        self.category_updater.update()

        self.assertEquals(self.category.count_children, 3-1)
        self.assertEquals(self.category.sum_children, 11-4)

    def test_child_added(self):
        self.category_updater.child_added(self.category, self.child)
        self.category_updater.update()

        self.assertEquals(self.category.count_children, 3+1)
        self.assertEquals(self.category.sum_children, 11+4)
import json

from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import now

from polls.controllers.import_controller.parent_category_updater import *
from polls.models import Category, Offer


class ParentCategoryUpdaterTest(TestCase):

    INITIAL_SUM = 11
    INITIAL_COUNT = 4
    INITIAL_OFFER_PRICE = 3
    LATER_DATE = now().replace(year=2222)

    def setUp(self):
        self.root_category = Category(sum_children=self.INITIAL_SUM, count_children=self.INITIAL_COUNT)
        self.root_category.save()
        self.child_category = Category(sum_children=self.INITIAL_SUM, count_children=self.INITIAL_COUNT, parent_category=self.root_category)
        self.child_category.save()
        self.child_offer = Offer(price=self.INITIAL_OFFER_PRICE, parent_category=self.child_category)
        self.child_offer.save()

    def test_child_offer_removed(self):
        parent_updater = ChildRemover(self.child_offer)

        parent_updater.update_parents()

        self.assertEquals(self.child_category.count_children, self.INITIAL_COUNT - 1)
        self.assertEquals(self.child_category.sum_children, self.INITIAL_SUM - self.INITIAL_OFFER_PRICE)
        self.assertEquals(self.root_category.count_children, self.INITIAL_COUNT - 1)
        self.assertEquals(self.root_category.sum_children, self.INITIAL_SUM - self.INITIAL_OFFER_PRICE)

    def test_child_offer_added(self):
        category_updater = ChildAdder(self.child_offer)
        category_updater.update_parents()

        self.assertEquals(self.child_category.count_children, self.INITIAL_COUNT + 1)
        self.assertEquals(self.child_category.sum_children, self.INITIAL_SUM + self.INITIAL_OFFER_PRICE)
        self.assertEquals(self.root_category.count_children, self.INITIAL_COUNT + 1)
        self.assertEquals(self.root_category.sum_children, self.INITIAL_SUM + self.INITIAL_OFFER_PRICE)

    def test_update_date_updated(self):
        self.child_offer.update_date = self.LATER_DATE
        category_updater = ChildAdder(self.child_offer)
        category_updater.update_parents()

        self.assertEquals(self.child_category.update_date, self.LATER_DATE)
        self.assertEquals(self.root_category.update_date, self.LATER_DATE)

    def test_update_date_not_updated_when_not_needed(self):
        self.child_offer.update_date = self.LATER_DATE
        category_updater = ChildAdder(self.child_offer)
        category_updater.update_parents()

        self.assertEquals(self.child_category.update_date, self.LATER_DATE)
        self.assertEquals(self.root_category.update_date, self.LATER_DATE)

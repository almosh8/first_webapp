from django.db import models
from django.utils.timezone import now
from polymorphic.models import PolymorphicModel


class Item(PolymorphicModel):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=200, default='unnamed')
    update_date = models.DateTimeField(default=now)

    # objects = InheritanceManager()

class ItemBuilder:

    def __init__(self):
        self.item = Item()

    def set_pk(self, pk):
        self.item.id = pk
        return self

    def set_name(self, name):
        self.item.name = name
        return self

    def set_update_date(self, update_date):
        self.item.update_date = update_date
        return self

    def set_parent_category(self, parent_category):
        self.item.parent_category = parent_category
        return self

    def set_price(self, price):

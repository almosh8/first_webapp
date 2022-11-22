from django.db import models

from polls.models.items.Category import Category
from polls.models.items.Item import Item


class Offer(Item):

    price = models.IntegerField(default=0)

    # moved this to parent class
    # parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, default=None)
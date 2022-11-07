from django.db import models

from polls.models.items.Item import Item


class Category(Item):
    sum_children = models.IntegerField(default=0)
    count_children = models.IntegerField(default=0)
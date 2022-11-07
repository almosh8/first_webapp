from django.db import models

from polls.models.items.Item import Item


class Offer(Item):
    price = models.IntegerField()
from django.db import models
from django.utils.timezone import now
from polymorphic.models import PolymorphicModel


class Item(PolymorphicModel):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=200, default='unnamed')
    update_date = models.DateTimeField(default=now)

    # objects = InheritanceManager()

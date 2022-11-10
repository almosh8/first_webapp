from django.db import models
from django.utils.timezone import now


class Item(models.Model):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=200, default='unnamed')
    update_date = models.DateTimeField(default=now)

    class Meta:
        abstract = True

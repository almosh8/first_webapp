from django.db import models
from django.utils.timezone import now


class Item(models.Model):
    id = models.CharField(max_length=99, primary_key=True, default=None)
    name = models.CharField(max_length=200, default=None)
    update_date = models.DateTimeField(default=now)

    class Meta:
        abstract = True

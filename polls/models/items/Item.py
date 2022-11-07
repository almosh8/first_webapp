from django.db import models
from django.utils.timezone import now


class Item(models.Model):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    update_date = models.DateTimeField(default=now)


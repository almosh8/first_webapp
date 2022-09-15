import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.utils.timezone import now

from polls.controllers.import_controller import ChildRemover, ChildAdder


class Category(models.Model):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    sum_children = models.IntegerField(default=0)
    count_children = models.IntegerField(default=0)
    update_date = models.DateTimeField(default=now)





    def commit(self):
        print(f'commiting {self.name}...')
        try:  # delete from previous parent
            old = Category.objects.get(pk=self.pk)
            old_parent = old.parent_category  # version of object before edit
            old_parent.remove_child(old)
            child_remover = ChildRemover(old)
            child_remover.update_parents()
            # TODO don't edit model twice when parent unchanged
        # ObjectDoesNotExist if item is just created
        # AttributeError if parent_category is None
        except (ObjectDoesNotExist, AttributeError):  # there was no parent before
            print(f'there was no parent of {self.name} before')
            pass

        try:  # add new version of object to new parent
            new_parent = Category.objects.get(pk=self.parent_category.pk)  # version of object before edit
            child_adder = ChildAdder(old)
            child_adder.update_parents()
        # AttributeError if parent_category is None
        except (AttributeError):  # there was no parent before
            print(f'there is no parent of {self.name} now')
            pass

        self.save()

    def get_children(self):
        # returns list of all child items
        offers = Offer.objects.filter(parent_category=self)
        categories = Category.objects.filter(parent_category=self)
        return list(offers) + list(categories)


class Offer(models.Model):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=300)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    update_date = models.DateTimeField(default=now)

    def commit(self):
        print(f'commiting {self.name}...')
        try:  # delete from previous parent
            old = Offer.objects.get(pk=self.pk) # version of object before edit
            old_parent = old.parent_category
            old_parent.remove_child(old)  # TODO don't edit model twice when parent unchanged
        # ObjectDoesNotExist if item is just created
        # AttributeError if parent_category is None
        except (ObjectDoesNotExist, AttributeError):  # there was no parent before
            print(f'there was no parent of {self.name} before')
            pass

        try:  # add new version of object to new parent
            new_parent = Category.objects.get(pk=self.parent_category.pk)  # parent object after edit
            new_parent.add_child(self)
        # AttributeError if parent_category is None
        except (AttributeError):  # there was no parent before
            print(f'there is no parent of {self.name} now')
            pass

        self.save()

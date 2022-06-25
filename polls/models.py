from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver


class Category(models.Model):
    id = models.CharField(max_length=99, primary_key=True)
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None)
    sum_children = models.IntegerField(default=0)
    count_children = models.IntegerField(default=0)
    update_date = models.DateTimeField(default=None)

    def average_price(self):
        try:
            return self.sum_children // self.count_children
        except ZeroDivisionError:
            return None

    def add_child(self, child):
        print(f'child {child.name} added to category {self.name}, before change sum={self.sum_children}')
        self.update_date = child.update_date  # assume child.update_date > self.update_date
        if isinstance(child, Offer):
            self.count_children += 1
            self.sum_children += child.price
            print(f'{child.name}({child.price}) added to {self.name}. sum now is {self.sum_children}')
        elif isinstance(child, Category):
            self.count_children += child.count_children
            self.sum_children += child.sum_children
            print(f'{child.name}({child.sum_children}) added to {self.name}. sum now is {self.sum_children}')
        else:
            raise TypeError
        self.save()

        if self.parent_category is not None:  # edit parent as well
            self.parent_category.add_child(child)

    def remove_child(self, child):
        print(f'child {child.name} removed from {self.name}, before change sum={self.sum_children}')
        self.update_date = child.update_date  # assume child.update_date > self.update_date
        if isinstance(child, Offer):
            self.count_children -= 1
            self.sum_children -= child.price
            print(f'{child.name}({child.price}) removed from {self.name}. sum now is {self.sum_children}')
        elif isinstance(child, Category):
            self.count_children -= child.count_children
            self.sum_children -= child.sum_children
            print(f'{child.name}({child.sum_children}) removed from {self.name}. sum now is {self.sum_children}')
        else:
            raise TypeError
        self.save()

        if self.parent_category is not None:  # edit parent as well
            self.parent_category.remove_child(child)

    def commit(self):
        print(f'commiting {self.name}...')
        try:  # delete from previous parent
            old = Category.objects.get(pk=self.pk)
            old_parent = old.parent_category  # version of object before edit
            old_parent.remove_child(old)  # TODO don't edit model twice when parent unchanged
        # ObjectDoesNotExist if item is just created
        # AttributeError if parent_category is None
        except (ObjectDoesNotExist, AttributeError):  # there was no parent before
            print(f'there was no parent of {self.name} before')
            pass

        try:  # add new version of object to new parent
            new_parent = Category.objects.get(pk=self.parent_category.pk)  # version of object before edit
            new_parent.add_child(self)
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
    update_date = models.DateTimeField(default=None)

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

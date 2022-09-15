from abc import abstractmethod, ABC

from django.core.exceptions import ObjectDoesNotExist

import polls.models
import operator


class ParentCategoryUpdater(ABC):

    #TODO don't use child as parameter

    def __init__(self, child):
        self.child = child
        self.parent_category = child.parent_category
        pass

    def update_parents(self):
        if self.parent_category is not None:
            self.__do_update()

    def __do_update(self):

        self.__update_counter()
        self.__set_latest_update_date()

        self.parent_category.save()

        self.__update_next_parent()

    def __update_counter(self):
        if isinstance(self.child, polls.models.Offer):
            self.parent_category.count_children = self.add_or_subtract(self.parent_category.count_children, 1)
            self.parent_category.sum_children = self.add_or_subtract(self.parent_category.sum_children,
                                                                     self.child.price)
        elif isinstance(self.child, polls.models.Category):
            self.parent_category.count_children = self.add_or_subtract(self.parent_category.count_children,
                                                                       self.child.count_children)
            self.parent_category.sum_children = self.add_or_subtract(self.parent_category.sum_children,
                                                                     self.child.sum_children)
        else:
            raise TypeError

    @abstractmethod
    def add_or_subtract(self, x, y):
        pass

    def __set_latest_update_date(self):
        if self.child.update_date > self.parent_category.update_date:
            self.parent_category.update_date = self.child.update_date

    # recursively update all parent categories
    def __update_next_parent(self):
        self.parent_category = self.parent_category.parent_category
        self.update_parents()


class ChildAdder(ParentCategoryUpdater):

    add_or_subtract = operator.add


class ChildRemover(ParentCategoryUpdater):

    add_or_subtract = operator.sub











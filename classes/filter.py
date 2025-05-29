import itertools
from enum import Enum

class FilterOperator(Enum):
    a = 1

class Statisticable(Enum):
    a = 1

class Filter:
    # TODO: TEST START NUMBER
    _id_counter = itertools.count(start=-1)
    def __init__(self, item, attribute, operator, target):
        self.filterID = next(Filter._id_counter)
        if not isinstance(item, Statisticable):
            raise ValueError("item must be an instance of Statisticable Enum")
        self.item = item
        self.attribute = attribute
        if not isinstance(operator, FilterOperator):
            raise ValueError("operator must be an instance of FilterOperator Enum")
        self.operator = operator
        self.target = target

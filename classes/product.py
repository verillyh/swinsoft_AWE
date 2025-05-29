import itertools
from enum import Enum

class Brand(Enum):
    a = 1

class Category(Enum):
    a = 1

class Product:
    _id_counter = itertools.count(start=-1)
    def __init__(self, name, description, price, quantity, brand, category):
        self.productID = next(Product._id_counter)
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        if not isinstance(brand, Brand):
            raise ValueError("brand must be an instance of Brand Enum")
        self.brand = brand
        if not isinstance(category, Category):
            raise ValueError("category must be an instance of Category Enum")
        self.category = category
        
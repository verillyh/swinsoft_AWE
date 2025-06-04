import itertools
from enum import Enum

class Brand(Enum):
    A = 1
    B = 2
    C = 3

class Category(Enum):
    Television = 1
    MobilePhone = 2
    Computer = 3

_id_counter = itertools.count(start=1)  # Auto-incrementing ID

class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int, category: Category, brand: Brand, productID: int = None):
        if productID is not None:
            self.id = int(productID)
        else:
            self.id = next(_id_counter)
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)
        if not isinstance(category, Category):
            raise ValueError("category must be a Category enum member")
        self.category = category

        if not isinstance(brand, Brand):
            raise ValueError("brand must be a Brand enum member")
        self.brand = brand

    def __str__(self):
        return (
            f"ID        : {self.id}\n"
            f"Name      : {self.name}\n"
            f"Brand     : {self.brand.name}\n"
            f"Category  : {self.category.name}\n"
            f"Price     : ${self.price:.2f}\n"
            f"Stock     : {self.quantity}\n"
            f"Description: {self.description}"
        )

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

class Product:
    _id_counter = itertools.count(start=1)  # Auto-incrementing ID

    def __init__(self, name: str, description: str, price: float, quantity: int, category: Category, brand: Brand):
        self.id = next(Product._id_counter)
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)
        category_enum = Category[category]
        if not isinstance(category_enum, Category):
            raise ValueError("category must be an instance of Category Enum")
        self.category = category_enum

        brand_enum = Brand[brand]
        if not isinstance(brand_enum, Brand):
            raise ValueError("brand must be an instance of Brand Enum")
        self.brand = brand_enum

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

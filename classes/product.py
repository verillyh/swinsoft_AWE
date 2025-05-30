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
        
        if not isinstance(category, Category):
            raise ValueError("category must be an instance of Category Enum")
        self.category = category

        if not isinstance(brand, Brand):
            raise ValueError("brand must be an instance of Brand Enum")
        self.brand = brand

    def __str__(self):
        return (f"Product[ID={self.id}, Name={self.name}, Description={self.description}, "
                f"Price=${self.price:.2f}, Quantity={self.quantity}, "
                f"Category={self.category.name}, Brand={self.brand.name}]")

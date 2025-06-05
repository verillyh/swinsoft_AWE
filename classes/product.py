import itertools
from enum import Enum

def load_brand_enum(db):
    rows = db.query("SELECT BrandName, BrandID FROM Brand;")
    members = {}
    for row in rows:
        if isinstance(row, dict):
            name = row["BrandName"]
            val = row["BrandID"]
        else:
            name, val = row
        safe_name = name.replace(" ", "_")
        members[safe_name] = val
    return Enum("Brand", members)

def Brand(db):
    return load_brand_enum(db)

def load_category_enum(db):
    rows = db.query("SELECT CategoryName, CategoryID FROM Category;")
    members = {}
    for row in rows:
        if isinstance(row, dict):
            name = row["CategoryName"]
            val = row["CategoryID"]
        else:
            name, val = row
        safe_name = name.replace(" ", "_")
        members[safe_name] = val
    return Enum("Category", members)

def Category(db):
    return load_category_enum(db)

_id_counter = itertools.count(start=1)

class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int, category: load_category_enum, brand: load_brand_enum, productID: int = None):
        self.id = productID if productID is not None else next(_id_counter)
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)
        self.category = category
        self.brand = brand

    @property
    def productID(self):
        return self.id
    
    @productID.setter
    def productID(self, value):
        self.id = value
    
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

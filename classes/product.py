import itertools
from enum import Enum

def Brand(db):
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

def Category(db):
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

class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int, category: Category, brand: Brand, productID: int = None):
        self.name = name
        self.product_id = productID
        self.description = description
        self.price = price
        self.quantity = quantity
        self.category = category
        self.brand = brand

    @property
    def productID(self):
        return self.product_id
    
    @productID.setter
    def productID(self, value):
        self.id = value
    
    def __str__(self):
        return (
            f"ID        : {self.product_id}\n"
            f"Name      : {self.name}\n"
            f"Brand     : {self.brand}\n"
            f"Category  : {self.category}\n"
            f"Price     : ${self.price:.2f}\n"
            f"Stock     : {self.quantity}\n"
            f"Description: {self.description}"
            "-------------"
        )

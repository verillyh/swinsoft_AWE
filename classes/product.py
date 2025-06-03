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

CATEGORY_ID_TO_ENUM = {
    1: Category.Television,
    2: Category.MobilePhone,
    3: Category.Computer
}
BRAND_ID_TO_ENUM = {
    1: Brand.A,
    2: Brand.B,
    3: Brand.C
}
CATEGORY_ENUM_TO_ID = {v: k for k, v in CATEGORY_ID_TO_ENUM.items()}
BRAND_ENUM_TO_ID = {v: k for k, v in BRAND_ID_TO_ENUM.items()}

class Product:
    _id_counter = itertools.count(start=1)

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 category: Category, brand: Brand, product_id=None):
        self._id = product_id if product_id is not None else next(Product._id_counter)
        self._name = name
        self._description = description
        self._price = float(price)
        self._quantity = int(quantity)

        if not isinstance(category, Category):
            raise ValueError("category must be a Category enum")
        if not isinstance(brand, Brand):
            raise ValueError("brand must be a Brand enum")

        self._category = category
        self._brand = brand

    def __str__(self):
        return (
            f"[{self._id}] {self._name}\n"
            f"Brand     : {self._brand.name}\n"
            f"Category  : {self._category.name}\n"
            f"Price     : ${self._price:.2f}\n"
            f"Stock     : {self._quantity}\n"
            f"Description: {self._description}"
        )

    # --- Getter methods ---
    def get_id(self): return self._id
    def get_name(self): return self._name
    def get_description(self): return self._description
    def get_price(self): return self._price
    def get_quantity(self): return self._quantity
    def get_category(self): return self._category
    def get_brand(self): return self._brand
    def get_brand_id(self): return BRAND_ENUM_TO_ID[self._brand]
    def get_category_id(self): return CATEGORY_ENUM_TO_ID[self._category]

    # --- Factory method for DB row ---
    @classmethod
    def from_db_row(cls, row):
        try:
            return cls(
                name=row[1],
                description=row[2],
                price=row[3],
                quantity=row[4],
                category=CATEGORY_ID_TO_ENUM[int(row[5])],
                brand=BRAND_ID_TO_ENUM[int(row[6])],
                product_id=row[0]
            )
        except Exception as e:
            raise ValueError(f"Error creating Product from DB row: {row}, reason: {e}")

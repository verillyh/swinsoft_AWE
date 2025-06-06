from abc import abstractmethod, ABC
from classes.product import Product

class ItemContainer(ABC):
    def __init__(self, product: list[Product], quantity: int, total_price: float, item_id = None):
        self.item_id = item_id
        self.product = product
        self.quantity = quantity
        self.total_price = total_price

    def get_total_price(self):
        return self.product["price"] * self.quantity

class CartItem(ItemContainer):
    def __init__(self, product: list[Product], quantity: int, total_price, is_selected: bool = False):
        super().__init__(product, quantity, total_price)
        self.is_selected = is_selected

    def set_cart_item_id(self, new_id: int):
        self.__cartItemID = new_id

    def get_cart_item_id(self):
        return self.__cartItemID

    def get_product(self):
        return self.product

    def get_quantity(self):
        return self._quantity

    def change_quantity(self, new_qty: int):
        self._quantity = new_qty
    
class OrderItem(ItemContainer):
    def __init__(self, product: list[Product], quantity: int, total_price: float):
        super().__init__(product, quantity, total_price)

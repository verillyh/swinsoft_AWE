from abc import abstractmethod, ABC
from classes.product import Product

class ItemContainer(ABC):
    def __init__(self, product: Product, quantity: int, total_price: float, item_id = None):
        self.item_id = item_id
        self.product = product
        self.quantity = quantity
        self.total_price = total_price

class CartItem(ItemContainer):
    def __init__(self, product: Product, quantity: int, total_price: float = None, is_selected: bool = False):
        total_price = product["price"] * quantity
        super().__init__(product, quantity, total_price)
        self.is_selected = is_selected
        
    def change_quantity(self, new_qty: int):
        self.quantity = new_qty
        self.total_price = self.product.price * self.quantity

    def get_total_price(self):
        return self.product.price * self.quantity
    
class OrderItem(ItemContainer):
    def __init__(self, product: list[Product], quantity: int, total_price: float):
        super().__init__(product, quantity, total_price)

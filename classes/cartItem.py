class CartItem:
    def __init__(self, product: dict, quantity: int):
        self._product = product
        self._quantity = quantity
        self.__cartItemID: int | None = None

    def set_cart_item_id(self, new_id: int):
        self.__cartItemID = new_id

    def get_cart_item_id(self):
        return self.__cartItemID

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def change_quantity(self, new_qty: int):
        self._quantity = new_qty

    def get_total_price(self):
        return self._product["price"] * self._quantity

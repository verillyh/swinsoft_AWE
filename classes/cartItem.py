class CartItem:
    def __init__(self, product: dict, quantity: int):
        self._product = product
        self._quantity = quantity
        self.__cartItemID: int | None = None

    def setCartItemID(self, new_id: int):
        self.__cartItemID = new_id

    def getCartItemID(self) -> int:
        return self.__cartItemID

    def getProduct(self) -> dict:
        return self._product

    def getQuantity(self) -> int:
        return self._quantity

    def changeQuantity(self, new_qty: int):
        self._quantity = new_qty

    def getTotalPrice(self) -> float:
        return self._product["price"] * self._quantity

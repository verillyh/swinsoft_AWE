import itertools

class CartItem:
    _id_counter = itertools.count(start=1)

    def __init__(self, product, quantity):
        self.__cartItemID = next(CartItem._id_counter)
        self.__quantity = quantity
        self.__product = product

    def getCartItemID(self):
        return self.__cartItemID

    def getProduct(self):
        return self.__product

    def getQuantity(self):
        return self.__quantity

    def getTotalPrice(self):
        return self.__product['price'] * self.__quantity

    def changeQuantity(self, newQty):
        self.__quantity = newQty

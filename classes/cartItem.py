<<<<<<< Updated upstream
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

    def changeItemQty(self, cartItemID, newQty):
        item = self.selectCartItem(cartItemID)
        if item:
            item.changeQuantity(newQty)
            return True
        return False 
=======
# from classes.itemContainer import ItemContainer
# class CartItem(ItemContainer):
#     def __init__(self, itemId, product, quantity):
#         super().__init__(itemId, product, quantity)
#         self.isSelected = False

#     def changeItemQty(self, cartItemID, newQty):
#         item = self.selectCartItem(cartItemID)
#         if item:
#             item.changeQuantity(newQty)
#             return True
#         return False 
    
#     def calculateTotalPrice(self):
#         return self.quantity * self.product['price']

# === classes/cartItem.py ===
from classes.itemContainer import ItemContainer
from classes.orderItem import OrderItem

class CartItem(ItemContainer):
    def __init__(self, itemId, quantity, product):
        super().__init__(itemId, quantity, product)
        self.isSelected = False

    def calculateTotalPrice(self):
        return self.quantity * self.product['price']

    def toOrderItem(self):
        return OrderItem(self.itemID, self.quantity, self.product)
>>>>>>> Stashed changes

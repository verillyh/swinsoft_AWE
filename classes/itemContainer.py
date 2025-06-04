# from abc import ABC, abstractmethod

# class ItemContainer(ABC):
#     def __init__(self, itemId: int, product, quantity: int):
#         self.itemId = itemId
#         self.quantity = quantity
#         self.product = product
#         self.totalPrice = self.calculateTotalPrice()

#     @abstractmethod
#     def calculateTotalPrice(self):
#         pass


# === classes/itemContainer.py ===
class ItemContainer:
    def __init__(self, itemId, quantity, product):
        self.itemID = itemId
        self.quantity = quantity
        self.product = product
        self.totalPrice = self.calculateTotalPrice()

    def getCartItemID(self):
        return self.itemID

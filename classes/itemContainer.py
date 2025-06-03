from abc import ABC, abstractmethod

class ItemContainer(ABC):
    def __init__(self, itemId: int, quantity: int, product):
        self.itemId = itemId
        self.quantity = quantity
        self.product = product
        self.totalPrice = self.calculateTotalPrice()

    @abstractmethod
    def calculateTotalPrice(self):
        pass
    def getTotalPrice(self):
        return self.totalPrice

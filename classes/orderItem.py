from classes.itemContainer import ItemContainer


class OrderItem(ItemContainer):
    def __init__(self, itemId, quantity, product):
        super().__init__(itemId, quantity, product)
        self.isSelected = False
 
    def calculateTotalPrice(self):
        return self.quantity * self.product.price

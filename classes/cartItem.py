from classes.itemContainer import ItemContainer
class CartItem(ItemContainer):
    def __init__(self, itemId, quantity, product):
        super().__init__(itemId, quantity, product)
        self.isSelected = False

    def changeItemQty(self, cartItemID, newQty):
        item = self.selectCartItem(cartItemID)
        if item:
            item.changeQuantity(newQty)
            return True
        return False 
    
    def calculateTotalPrice(self):
        return self.quantity * self.product.price
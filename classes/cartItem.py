import itertools

class CartItem:
    _id_counter = itertools.count(start=-1)
    def __init__(self, quantity):
        self.cartItemID = next(CartItem._id_counter)
        self.quantity = quantity
        self.isSelected = False

    def getTotalPrice():

        return False
    
    def changeQuantity():

        return False
    
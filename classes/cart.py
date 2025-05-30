import itertools
from classes.cartItem import CartItem

class Cart:
    __id_counter = itertools.count(start=1)

    def __init__(self):
        self.__cartID = next(Cart.__id_counter)
        self.__cartItems = []

    def addToCart(self, product, quantity):
        for item in self.__cartItems:
            if item.getProduct()['id'] == product['id']:
                item.changeQuantity(item.getQuantity() + quantity)
                return True
            
        newItem = CartItem(product, quantity)
        self.__cartItems.append(newItem)
        return True
    
    def removeCartItem(self, cartItemID):
        for item in self.__cartItems:
            if item.getCartItemID() == cartItemID:
                self.__cartItems.remove(item)
                return True
        return False
    
    def selectCartItem(self, cartItemID):
        for item in self.__cartItems:
            if item.getCartItemID() == cartItemID:
                return item
        return None
    
    def changeItemQty(self, cartItemID, newQty):
        item = self.selectCartItem(cartItemID)
        if item:
            item.changeQuantity(newQty)
            return True
        return False 
    
    def listProductsInCart(self):
        if not self.__cartItems:
            return "Cart is empty"
        lines = []
        for item in self.__cartItems:
            lines.append(f"Product: {item.getProduct()['name']} x {item.getQuantity()} = ${item.getTotalPrice()}")
        return "\n".join(lines)
    
    def checkout(self):
        if not self.__cartItems:
            return 0
        total = sum(item.getTotalPrice() for item in self.__cartItems)
        self.__cartItems.clear()
        return total
    
    

import itertools
from classes.cartItem import CartItem

class Cart:
    __id_counter = itertools.count(start=1)

    def __init__(self):
        self.__cartID = next(Cart.__id_counter)
        self.__cartItems = []
        self.customer_id = 0

    def addToCart(self, product, quantity):
        for item in self.__cartItems:
            if item.product['id'] == product['id']:
                item.changeQuantity(item.quantity + quantity)
                return True
        new_id = next(self.__id_counter)
        newItem = CartItem(new_id, product, quantity)
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
    
    
    def listProductsInCart(self):
        if not self.__cartItems:
            return "Cart is empty"
        lines = []
        for item in self.__cartItems:
            lines.append(f"Product: {item.product['name']} x {item.quantity} = ${item.calculateTotalPrice():.2f}")
        return "\n".join(lines)
    
    def checkout(self):
        if not self.__cartItems:
            return 0
        total = sum(item.calculateTotalPrice() for item in self.__cartItems)
        self.__cartItems.clear()
        return total
 
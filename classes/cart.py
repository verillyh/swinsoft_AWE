import itertools
from classes.cartItem import CartItem
from classes.payment import Payment
from classes.order import Order, OrderStatus

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
    def cartUI(self):
        print("#" + "=" * 50)
        print(f"{'YOUR CART':^52}")
        print("#" + "=" * 50)
        
        cart_items = self._Cart__cartItems  # Accessing private attribute (or make a getter)
        if not cart_items:
            print("Cart is empty.\n")
        else:
            for item in cart_items:
                prod = item.getProduct()
                print(f"[{prod['id']}] {prod['name']} - ${prod['price']} x {item.getQuantity()}")

            total = sum(item.getTotalPrice() for item in cart_items)
            print(f"\nTotal: ${total}")

        print("\n[1] Remove Item")
        print("[2] Update Quantity")
        print("[3] Proceed to Checkout")
        print("[0] Return to Menu")
        print("[X] Return to Previous Page")

    def removeItemUI(self):
        try:
            cartItemID = int(input("\n// Choice 3.[1]\n\nEnter Product ID to remove: "))
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == "y":
                if self.removeCartItem(cartItemID):
                    print("Item removed successfully.\n")
                else:
                    print("Item not found.\n")
            else:
                print("Cancelled.\n")
        except ValueError:
            print("Invalid input.\n")

    def getCartItems(self):
        return self.__cartItems

    def checkoutUI(self):
        if not self.getCartItems():
            print("Cart is empty. Cannot proceed to checkout.")
            return

        print("#" + "=" * 50)
        print(f"{'CHECKOUT':^52}")
        print("#" + "=" * 50)

        # Shipping details
        print("\n# " + "=" * 50)
        print(f"{'ENTER SHIPPING DETAILS':^52}")
        print("# " + "=" * 50)
        full_name = input("Full Name         : ")
        phone_number = input("Phone Number      : ")
        address = input("Shipping Address  : ")

        # Payment details
        print("\n# " + "=" * 50)
        print(f"{'ENTER PAYMENT DETAILS':^52}")
        print("# " + "=" * 50)
        cardholder_name = input("Cardholder Name   : ")
        card_number = input("Card Number       : ")
        expiry = input("Expiry (MM/YY)    : ")
        cvv = input("CVV               : ")

        try:
            expiry_month, expiry_year = map(int, expiry.split("/"))
            cvv_int = int(cvv)
        except ValueError:
            print("Invalid expiry or CVV format.")
            return

        payment = Payment()
        transaction_id = payment.requestPaymentFromVendor(card_number, expiry_month, expiry_year, cvv_int)

        if not payment.validateTransaction(transaction_id):
            print("Payment failed. Transaction invalid.")
            return

        order = Order(customerId=self.customer_id, items=self.cart.getCartItems(), orderStatus=OrderStatus.PAID)

        # Invoice
        print("\n# " + "=" * 50)
        print(f"{'INVOICE':^52}")
        print("# " + "=" * 50)
        print("-" * 30)
        for item in order.getItems():
            prod = item.getProduct()
            print(f"{prod['name']} x{item.getQuantity()} - ${item.getTotalPrice()}")
        print(f"Total: ${order.getTotalCost()}")

        choice = input("\n[1] Place the order\n[0] to Cancel\n\nEnter choice: ")
        if choice.strip() == "1":
            self.cart.getCartItems().clear()
            order.notifyStaff()
            print("\n" + payment.generateReceipt(order))
        else:
            print("Order cancelled.")
  

    
    
    

    

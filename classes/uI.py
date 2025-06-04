from classes.order import Order, OrderStatus
from classes.orderItem import OrderItem
from classes.payment import Payment
from classes.invoice import Invoice

class ClassUI:
    def __init__(self, cart, customer_id):
        self.cart = cart
        self.customer_id = customer_id

    def cartUI(self):
        print("#" + "=" * 50)
        print(f"{'YOUR CART':^52}")
        print("#" + "=" * 50)

        cart_items = self.cart.getCartItems()
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
                if self.cart.removeCartItem(cartItemID):
                    print("Item removed successfully.\n")
                else:
                    print("Item not found.\n")
            else:
                print("Cancelled.\n")
        except ValueError:
            print("Invalid input.\n")

    def checkoutUI(self):
        if not self.cart.getCartItems():
            print("Cart is empty. Cannot proceed to checkout.")
            return
        
        print("\n# " + "=" * 50)
        print(f"{'ENTER SHIPPING DETAILS':^52}")
        print("# " + "=" * 50)
        full_name = input("Full Name         : ")
        phone_number = input("Phone Number      : ")
        address = input("Shipping Address  : ")
        print("\nShipping info recorded successfully.")

        choice = input("\n[1] Place the order\n[0] Cancel\n\nEnter choice: ")
        if choice.strip() != "1":
            print("Order cancelled.")
            return

        order, invoice = self.cart._Cart__placeOrder()

        print(invoice)

        choice = input("\n[1] Pay the invoice\n[0] Cancel\n\nEnter choice: ")
        if choice.strip() != "1":
            print("Order cancelled.")
            return

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

        invoice.payInvoice()
        order.updateStatus(updaterAccountId=0, status=OrderStatus.PAID)
        order.notifyStaff()
        print("\n" + str(payment.generateReceipt(invoice)))

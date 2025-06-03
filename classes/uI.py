class CartUI:

    def __init__(self, cart, customer_id):
        self.cart = cart
        self.customer_id = customer_id
    def cartUI(self):
        print("#" + "=" * 50)
        print(f"{'YOUR CART':^52}")
        print("#" + "=" * 50)
        
        cart_items = self._Cart__cartItems 
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
        
        print("\n# " + "=" * 50)
        print(f"{'INVOICE':^52}")
        print("# " + "=" * 50)
        print("-" * 30)

        for item in self.getCartItems():
            prod = item.getProduct()
            print(f"{prod['name']} x{item.getQuantity()} - ${item.getTotalPrice()}")
        total = sum(item.getTotalPrice() for item in self.getCartItems())
        print(f"Total: ${total}")
            
        choice = input("\n[1] Pay the invoice\n[0] Cancel\n\nEnter choice: ")
        if choice.strip() != "1":
            print("Order cancelled.")
            return

        order = Order(customerId=self.customer_id, items=self.getCartItems(), orderStatus=OrderStatus.PENDING)

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

        order.updateStatus(updaterAccoutnId=0, status=OrderStatus.PAID)
        self.getCartItems().clear()
        order.notifyStaff()
        print("\n" + payment.generateReceipt(order))

    if __name__ == "__main__":
        cart_items = [
            ("Product_1", 1, 320.00),
            ("Product_4", 2, 180.00)
        ]

        invoice = Invoice(cart_items)

        # 1. Print the invoice
        print(invoice)

        # 2. Ask user to process the order
        choice = input("\n[1] Place the order\n[0] to Cancel\nYour choice: ")

        if choice == "1":
            if invoice.payInvoice():
                print("Order placed successfully.")
                
                # 3. Generate and print receipt
                receipt = Receipt(invoice)
                print(receipt)
            else:
                print("Invoice was already paid.")
        elif choice == "0":
            print("Order cancelled.")
        else:
            print("Invalid input. Order not processed.")


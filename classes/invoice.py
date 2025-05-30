import itertools
from receipt import Receipt


class Invoice:
    _id_counter = itertools.count(start=1)

    def __init__(self, items):
        self.invoiceID = next(Invoice._id_counter)
        self.isPaid = False
        self.items = items  # List of tuples: (product_name, quantity, price)

    def payInvoice(self):
        if not self.isPaid:
            self.isPaid = True
            return True
        return False

    def __str__(self):
        output = "\n# ==================================================\n"
        output += "                INVOICE\n"
        output += "# ==================================================\n"
        total = 0
        for name, qty, price in self.items:
            line_total = qty * price
            output += f"{name} x{qty} — ${line_total:.2f}\n"
            total += line_total
        output += f"Total: ${total:.2f}\n"
        return output

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

import itertools

class Receipt:
    _id_counter = itertools.count(start=1)

    def __init__(self, items):
        self.receiptID = next(Receipt._id_counter)
        self.items = items  # list of tuples: (product_name, quantity, price)

    def __str__(self):
        output = "\n========== RECEIPT ==========\n"
        output += f"Receipt ID: {self.receiptID}\n"
        total = 0
        for name, qty, price in self.items:
            line_total = qty * price
            output += f"{name} x{qty} — ${line_total:.2f}\n"
            total += line_total
        output += f"Total Paid: ${total:.2f}\n"
        output += "=============================\n"
        return output

if __name__ == "__main__":
    cart_items = [
        ("Product_1", 1, 300.00),
        ("Product_4", 2, 150.00)
    ]

    receipt = Receipt(cart_items)
    print(receipt)

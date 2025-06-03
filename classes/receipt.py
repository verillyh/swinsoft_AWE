from product import Product
from order import Order

class Receipt:
    def __init__(self, receiptID: int, orderContents: Order):
        self.receiptID = receiptID
        self.orderContents = orderContents

    def __str__(self):
        output = f"\n# ==================================================\n"
        output += f"RECEIPT ID: {self.receiptID}\n"
        output += "# ==================================================\n"
        for item in self.orderContents.items:
            product: Product = item.product
            output += (
                f"{product.get_name()} x{item.quantity} — ${product.get_price() * item.quantity:.2f}\n"
            )
        output += f"Total: ${self.orderContents.totalCost:.2f}\n"
        return output
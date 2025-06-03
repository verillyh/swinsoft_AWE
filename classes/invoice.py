from order import Order
class Invoice:
    def __init__(self, invoiceID: int, orderContents: Order, isPaid: bool = False):
        self.invoiceID = invoiceID
        self.orderContents = orderContents
        self.isPaid = isPaid

    def payInvoice(self) -> bool:
        self.isPaid = True
        return self.isPaid

    def __str__(self):
        output = f"\n# ==================================================\n"
        output += f"INVOICE ID: {self.invoiceID}\n"
        output += "# ==================================================\n"
        for item in self.orderContents.items:
            product: Product = item.product
            output += (
                f"{product.get_name()} x{item.quantity} — ${product.get_price() * item.quantity:.2f}\n"
            )
        output += f"Total: ${self.orderContents.totalCost:.2f}\n"
        output += f"Status: {'PAID' if self.isPaid else 'UNPAID'}\n"
        return output

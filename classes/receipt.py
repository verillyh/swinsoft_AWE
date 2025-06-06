import itertools

class Receipt:
    _id_counter = itertools.count(start=1)

    def __init__(self, invoice):
        self.receiptID = next(Receipt._id_counter)
        self.invoiceID = invoice.invoice_id
        self.items = invoice.order_contents

    def __str__(self):
        output = "\n========== RECEIPT ==========\n"
        output += f"Receipt ID: {self.receiptID}\n"
        output += f"From Invoice: {self.invoiceID}\n"
        # total = self.items.total_cost
        # print(self.items)
        # for name, qty, price in self.items:
        #     line_total = qty * price
        #     output += f"{name} x{qty} — ${line_total:.2f}\n"
        #     total += line_total
        output += f"Total Paid: ${total:.2f}\n"
        output += "=============================\n"
        return output

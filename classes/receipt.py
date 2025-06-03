import itertools
from classes.invoice import Invoice

class Receipt:
    _id_counter = itertools.count(start=1)

    def __init__(self, invoice: Invoice):
        self.receiptID = next(Receipt._id_counter)
        self.__invoice = invoice
        self.items = invoice.items  

    def __str__(self):
        output = "\n========== RECEIPT ==========\n"
        output += f"Receipt ID: {self.receiptID}\n"
        output += f"From Invoice: {self.__invoice.invoiceID}\n"
        total = 0
        for name, qty, price in self.items:
            line_total = qty * price
            output += f"{name} x{qty} — ${line_total:.2f}\n"
            total += line_total
        output += f"Total Paid: ${total:.2f}\n"
        output += "=============================\n"
        return output

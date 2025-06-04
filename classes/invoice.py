# import itertools
# from classes.order import Order

# class Invoice:
#     _id_counter = itertools.count(start=1)

#     def __init__(self, order: Order):
#         self.invoiceID = next(Invoice._id_counter)
#         self.isPaid = False
#         self.__orderContent = order
#         self.items = [
#             (item.product['name'], item.quantity, item.product['price'])
#             for item in self.__orderContent.items
#         ]
#     def payInvoice(self):
#         if not self.isPaid:
#             self.isPaid = True
#             return True
#         return False

#     def __str__(self):
#         output = "\n# ==================================================\n"
#         output += "                INVOICE\n"
#         output += "# ==================================================\n"
#         total = 0
#         for name, qty, price in self.items:
#             line_total = qty * price
#             output += f"{name} x{qty} — ${line_total:.2f}\n"
#             total += line_total
#         output += f"Total: ${total:.2f}\n"
#         return output

# === classes/invoice.py ===
import itertools

class Invoice:
<<<<<<< Updated upstream
    _id_counter = itertools.count(start=-1)
    def __init__(self):
        self.invoiceID = next(Invoice._id_counter)
        self.isPaid = False

    def payInvoice():

        return False
    
=======
    _id_counter = itertools.count(start=1)

    def __init__(self, order):
        self.invoiceID = next(Invoice._id_counter)
        self.isPaid = False
        self.__orderContent = order
        self.items = [
            (item.product['name'], item.quantity, item.product['price'])
            for item in self.__orderContent.items
        ]

    def payInvoice(self):
        if not self.isPaid:
            self.isPaid = True
            return True
        return False

    def __str__(self):
        output = "\n# ==================================================\n"
        output += "                     INVOICE\n"
        output += "# ==================================================\n"
        total = 0
        for name, qty, price in self.items:
            line_total = qty * price
            output += f"{name} x{qty} — ${line_total:.2f}\n"
            total += line_total
        output += f"Total: ${total:.2f}\n"
        return output
>>>>>>> Stashed changes

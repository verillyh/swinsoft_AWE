import itertools

class Invoice:
    _id_counter = itertools.count(start=-1)
    def __init__(self):
        self.invoiceID = next(Invoice._id_counter)
        self.isPaid = False

    def payInvoice():

        return False
    
import itertools

class Receipt:
    _id_counter = itertools.count(start=-1)
    def __init__(self):
        self.receiptID = next(Receipt._id_counter)

class main:
    receipt1 = Receipt()
    print(receipt1._id_counter)
    receipt2 = Receipt()
    print(receipt2._id_counter)

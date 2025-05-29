import itertools
import datetime as dt
from enum import Enum

class OrderStatus(Enum):
    a = 1

class Order:
    _id_counter = itertools.count(start=-1)
    def __init__(self, orderStatus):
        self.orderID = next(Order._id_counter)
        self.items = []
        self.datetime = dt.now
        if not isinstance(orderStatus, OrderStatus):
            raise ValueError("orderStatus must be an instance of OrderStatus Enum")
        self.orderStatus = orderStatus

    def notifyStaff():
        
        return False
    
    def updateStatus():

        return False
        
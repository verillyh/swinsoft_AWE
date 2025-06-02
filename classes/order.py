import itertools
import datetime as dt
from enum import Enum

class OrderStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class Order:
    _id_counter = itertools.count(start=-1)
    def __init__(self, customerId: int, items: list, orderStatus: OrderStatus = OrderStatus.PENDING):
        self.__orderID = next(Order._id_counter)
        self.__customerID = customerId
        self.__receiptID = None
        self.__invoiceID = None
        self.__items = items
        self.__datetime = dt.datetime.now

        if not isinstance(orderStatus, OrderStatus):
            raise ValueError("orderStatus must be an instance of OrderStatus Enum")
        self.__orderStatus = orderStatus

        self.__totalCost = sum(item.getTotalPrice() for item in items)
    
    def getOrderId(self):
        return self.__orderID

    def getTotalCost(self):
        return self.__totalCost
    
    def getItems(self):
        return self.__items
    
    def notifyStaff(self):
        print(f"Staff notified: Order #{self.__orderID} has been placed by Customer #{self.__customerID}.")
        return True
    
    def updateStatus(self, updaterAccoutnId: int, status: OrderStatus ):
        if not isinstance(status, OrderStatus):
            raise ValueError("status must be an instance of OrderStatus Enum")
        print(f"Order #{self.__orderID} status updated by Account #{updaterAccoutnId}: {self.__orderStatus.value}  -> {status.value}")
        self.__orderStatus = status
        return True
        
    
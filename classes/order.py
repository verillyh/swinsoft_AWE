import itertools
import datetime as dt
from enum import Enum
from classes.orderItem import OrderItem

class OrderStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"

class Order:
    _id_counter = itertools.count(start=-1)
    def __init__(self, customerId: int, items: list, orderStatus: OrderStatus = OrderStatus.PENDING):
        self.orderID = next(Order._id_counter)
        self.__customerID = customerId
        self.items = list(items) 
        self.datetime = dt.datetime.now()

        if not isinstance(orderStatus, OrderStatus):
            raise ValueError("orderStatus must be an instance of OrderStatus Enum")
        self.orderStatus = orderStatus

        self.totalCost = sum(item.getTotalPrice() for item in items)
    
    def notifyStaff(self):
        print(f"Staff notified: New order #{self.__orderID} placed at {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        return True
    
    def updateStatus(self, updaterAccountId: int, status: OrderStatus ):
        if not isinstance(status, OrderStatus):
            raise ValueError("status must be an instance of OrderStatus Enum")
        print(f"Order #{self.orderID} status updated by Account #{updaterAccountId}: {self.orderStatus.value}  -> {status.value}")
        self.orderStatus = status
        return True
        
    
import itertools
import datetime as dt
from enum import Enum
from classes.cartItem import CartItem
from classes.inboxMessage import InboxMessage

class OrderStatus(Enum):
    PENDING   = "PENDING"
    PAID      = "PAID"
    SHIPPED   = "SHIPPED"
    CANCELLED = "CANCELLED"

_id_counter = itertools.count(start=-1)

class Order:
    def __init__(self, customerId: int, items: list, orderStatus: OrderStatus = OrderStatus.PENDING, orderID = None, *, customername: str, phoneNumber: str, shippingAddress: str):
        self.__orderID = int(orderID) if orderID is not None else next(_id_counter)
        self.__customerID = customerId
        self.__receiptID  = None
        self.__invoiceID  = None
        self.__items      = items
        self.__datetime   = dt.datetime.now()
        self.__customerName = customername
        self.__phoneNumber = phoneNumber
        self.__shippingAddress = shippingAddress
        self.__totalCost = sum(item.getTotalPrice() for item in items)

        if not isinstance(orderStatus, OrderStatus):
            raise ValueError("orderStatus must be an instance of OrderStatus Enum")
        self.__orderStatus = orderStatus

    @property
    def orderID(self):
        return self.__orderID

    @orderID.setter
    def orderID(self, value):
        self.__orderID = value

    @property
    def orderStatus(self):
        return self.__orderStatus

    @orderStatus.setter
    def orderID(self, value):
        self.__orderStatus = value

    def getTotalCost(self):
        return self.__totalCost

    def getItems(self):
        return self.__items

    def update_status_db(self, db, new_status: OrderStatus, staff_list: list, customer_account):
        update_sql = """
            UPDATE orderrecord
            SET OrderStatus = %s
            WHERE OrderID = %s;
        """
        db.query(update_sql, (new_status.value, self.__orderID))
        self.__orderStatus = new_status

        if new_status == OrderStatus.PAID:
            staff_message = f"Order #{self.__orderID} has been marked PAID."
            for staff in staff_list:
                staff.inbox.append(InboxMessage(staff_message))

            customer_message = f"Your Order #{self.__orderID} has been placed and paid."
            customer_account.inbox.append(InboxMessage(customer_message))
    
    @classmethod
    def fetch_by_customer(cls, customer_id: int, db):
        sql = """
          SELECT 
            o.OrderID,
            o.CustomerID,
            o.OrderDate,
            o.ShippingAddress,
            o.OrderStatus,
            i.ProductID,
            i.Quantity,
            i.UnitPrice,
            p.Name AS ProductName
          FROM orderrecord o
          JOIN orderitem i ON o.OrderID = i.OrderID
          JOIN productgood p ON i.ProductID = p.ProductID
          WHERE o.CustomerID = %s
          ORDER BY o.OrderDate DESC, o.OrderID DESC;
        """
        rows = db.query(sql, (customer_id,))
        if not rows:
            return []

        grouped = {}
        for row in rows:
            oid = row["OrderID"]
            if oid not in grouped:
                grouped[oid] = {
                    "customerID": row["CustomerID"],
                    "orderID":    row["OrderID"],
                    "orderDate":  row["OrderDate"],
                    "shipping":   row["ShippingAddress"],
                    "status":     OrderStatus(row["OrderStatus"]),
                    "items":      [],
                }
            line_item = {
                "id":    row["ProductID"],
                "name":  row["ProductName"],
                "price": row["UnitPrice"],
            }
            ci = CartItem(line_item, row["Quantity"])
            grouped[oid]["items"].append(ci)

        result = []
        for data in grouped.values():
            order = Order(
                data["customerID"],
                data["items"],
                data["status"],
                orderID=data["orderID"],
                customername="",
                phoneNumber="",
                shippingAddress=data["shipping"],
            )
            order._Order__datetime = data["orderDate"]
            result.append(order)
        return result

    @classmethod
    def fetch_all(cls, db):
        sql = """
          SELECT 
            o.OrderID,
            o.CustomerID,
            o.OrderDate,
            o.ShippingAddress,
            o.OrderStatus,
            i.ProductID,
            i.Quantity,
            i.UnitPrice,
            p.Name AS ProductName
          FROM orderrecord o
          JOIN orderitem i ON o.OrderID = i.OrderID
          JOIN productgood p ON i.ProductID = p.ProductID
          ORDER BY o.OrderDate DESC, o.OrderID DESC;
        """
        rows = db.query(sql)
        if not rows:
            return []

        grouped = {}
        for row in rows:
            oid = row["OrderID"]
            if oid not in grouped:
                grouped[oid] = {
                    "customerID": row["CustomerID"],
                    "orderID":    row["OrderID"],
                    "orderDate":  row["OrderDate"],
                    "shipping":   row["ShippingAddress"],
                    "status":     OrderStatus(row["OrderStatus"]),
                    "items":      [],
                }
            line_item = {
                "id":    row["ProductID"],
                "name":  row["ProductName"],
                "price": row["UnitPrice"],
            }
            ci = CartItem(line_item, row["Quantity"])
            grouped[oid]["items"].append(ci)

        result = []
        for data in grouped.values():
            order = Order(
                data["customerID"],
                data["items"],
                data["status"],
                orderID=data["orderID"],
                customername="",
                phoneNumber="",
                shippingAddress=data["shipping"],
            )
            order._Order__datetime = data["orderDate"]
            result.append(order)
        return result
    
    def __str__(self):
        lines = []
        lines.append(f"Order ID   : {self.__orderID}")
        lines.append(f"Date/Time  : {self.__datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"CustomerID : {self.__customerID}")
        lines.append(f"Status     : {self.__orderStatus.value}")
        lines.append(f"Total Cost : ${self.__totalCost:.2f}")
        lines.append("Items:")
        for ci in self.__items:
            prod = ci.getProduct()
            name = prod["name"]
            qty = ci.getQuantity()
            price = prod["price"]
            lines.append(f"  - {name} x{qty} @ ${price:.2f} each → ${qty*price:.2f}")
        return "\n".join(lines)

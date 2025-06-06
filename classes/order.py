import datetime as dt
from enum import Enum
from classes.itemContainer import CartItem
from classes.inboxMessage import InboxMessage
from classes.itemContainer import OrderItem

class OrderStatus(Enum):
    PENDING   = "PENDING"
    PAID      = "PAID"
    SHIPPED   = "SHIPPED"
    CANCELLED = "CANCELLED"

class Order:
    def __init__(self, customer_id: int, items: list[OrderItem], orderStatus: OrderStatus = OrderStatus.PENDING, order_id = None, *, phone_number: str, delivery_address: str):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.datetime   = dt.datetime.now()
        self.phone_number = phone_number
        self.delivery_address = delivery_address
        self.total_cost = sum(item.get_total_price() for item in items)

        if not isinstance(orderStatus, OrderStatus):
            raise ValueError("orderStatus must be an instance of OrderStatus Enum")
        self.orderStatus = orderStatus

    @property
    def orderID(self):
        return self.order_id

    @orderID.setter
    def orderID(self, value):
        self.order_id = value

    @property
    def orderStatus(self):
        return self.orderStatus

    @orderStatus.setter
    def orderStatus(self, value):
        self.orderStatus = value

    def get_total_cost(self):
        return self.totalCost

    def get_items(self):
        return self.items

    def change_status(self, db, new_status: OrderStatus):
        update_sql = """
            UPDATE order_record
            SET OrderStatus = %s
            WHERE OrderID = %s;
        """
        db.query(update_sql, (new_status.value, self.order_id))
        self.orderStatus = new_status

        # if new_status == OrderStatus.PAID:
        #     staff_message = f"Order #{self.order_id} has been marked PAID."
        #     for staff in staff_list:
        #         staff.inbox.append(InboxMessage(staff_message))

        #     customer_message = f"Your Order #{self.order_id} has been placed and paid."
        #     customer_account.inbox.append(InboxMessage(customer_message))
    
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
          FROM order_record o
          JOIN order_item i ON o.OrderID = i.OrderID
          JOIN product_good p ON i.ProductID = p.ProductID
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
          FROM order_record o
          JOIN order_item i ON o.OrderID = i.OrderID
          JOIN product_good p ON i.ProductID = p.ProductID
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
        lines.append(f"Order ID   : {self.order_id}")
        lines.append(f"Date/Time  : {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"CustomerID : {self.customer_id}")
        lines.append(f"Status     : {self.orderStatus.value}")
        lines.append(f"Total Cost : ${self.totalCost:.2f}")
        lines.append("Items:")
        for ci in self.__items:
            prod = ci.getProduct()
            name = prod["name"]
            qty = ci.getQuantity()
            price = prod["price"]
            lines.append(f"  - {name} x{qty} @ ${price:.2f} each → ${qty*price:.2f}")
        return "\n".join(lines)

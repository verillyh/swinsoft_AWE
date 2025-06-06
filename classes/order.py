import datetime as dt
from enum import Enum
from classes.itemContainer import CartItem
from classes.inboxMessage import InboxMessage
from classes.itemContainer import OrderItem
from classes.product import Product

class OrderStatus(Enum):
    PENDING   = "PENDING"
    PAID      = "PAID"
    SHIPPED   = "SHIPPED"
    CANCELLED = "CANCELLED"

class Order:
    def __init__(self, customer_id: int, items: list[OrderItem], order_status: OrderStatus = OrderStatus.PENDING, order_id = None, *, phone_number: str, delivery_address: str, total_cost = None):
        self.order_id = order_id
        self.customer_id = customer_id
        self.items = items
        self.datetime   = dt.datetime.now()
        self.phone_number = phone_number
        self.delivery_address = delivery_address
        
        total_costs = []

        for item in items:
            total_costs.append(item.total_price)

        self.total_cost = sum(total_costs)

        if not isinstance(order_status, OrderStatus):
            raise ValueError("orderStatus must be an instance of OrderStatus Enum")
        self.orderStatus = order_status

    @property
    def orderID(self):
        return self.order_id

    @orderID.setter
    def orderID(self, value):
        self.order_id = value

    @property
    def orderStatus(self):
        return self.order_status

    @orderStatus.setter
    def orderStatus(self, value):
        self.order_status = value

    def get_total_cost(self):
        return self.totalCost

    def get_items(self):
        return self.items

    def change_status(db, order_id: int, new_status: OrderStatus):
        update_sql = """
            UPDATE order_record
            SET OrderStatus = %s
            WHERE OrderID = %s;
        """
        db.query(update_sql, (new_status.value, order_id))
    
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
            p.Name AS ProductName,
            p.Description,
            p.BrandID,
            p.CategoryID
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
            line_item = Product(
                productID=row["ProductID"],
                name=row["ProductName"],
                price=row["UnitPrice"],
                description=row["Description"],
                quantity=row["Quantity"],
                category=row["CategoryID"],
                brand=row["BrandID"]
            )
        
            ci = CartItem(line_item, row["Quantity"])
            grouped[oid]["items"].append(ci)

        result = []
        for data in grouped.values():
            order = Order(
                data["customerID"],
                data["items"],
                data["status"],
                order_id=data["orderID"],
                phone_number="",
                delivery_address=data["shipping"],
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
                order_id=data["orderID"],
                phone_number="",
                delivery_address=data["shipping"],
            )
            order._Order__datetime = data["orderDate"]
            result.append(order)
        return result
    
    def total_cost(self) -> float:
        return sum(item.quantity * item.product.price for item in self.items)

    def print_items(self, indent: int = 0) -> str:
        pad = " " * indent
        if not self.items:
            return pad + "(No items)"
        header = f"{pad}ProductID | ProductName       | Qty | UnitPrice | LineTotal"
        divider= pad + "-" * len(header)
        lines = [header, divider]
        for item in self.items:
            pid        = item.product.product_id
            pname      = item.product.name
            qty        = item.quantity
            unit_price = item.product.price
            line_total = qty * unit_price
            lines.append(
                f"{pad}{pid:<9} | {pname:<18} | {qty:>3} | "
                f"${unit_price:>8.2f} | ${line_total:>8.2f}"
            )
        return "\n".join(lines)
    
    def __str__(self):
        lines = []
        lines.append(f"Order ID   : {self.order_id}")
        lines.append(f"Date/Time  : {self.datetime.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"CustomerID : {self.customer_id}")
        lines.append(f"Status     : {self.orderStatus.value}")
        lines.append(f"Total Cost : ${self.total_cost:.2f}")
        lines.append("Items:")
        for ci in self.items:
            prod = ci.product
            name = prod["name"]
            qty = ci.quantity
            price = prod["price"]
            lines.append(f"  - {name} x{qty} @ ${price:.2f} each → ${qty*price:.2f}")
        return "\n".join(lines)

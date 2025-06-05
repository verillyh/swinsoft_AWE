import itertools
from classes.cartItem import CartItem
from classes.payment import Payment
from classes.order import Order, OrderStatus
from classes.product import Product

class Cart:
    def __init__(self, customerID):
        self.customer_id = customerID
        self._items: list[CartItem] = []

    def _reassignIDs(self):
        for idx, item in enumerate(self._items, start=1):
            item.setCartItemID(idx)

    def clear_cart(self):
        self._items.clear()
        self._reassignIDs()

    # def _fetchCartRows(self):
    #     select_sql = """
    #         SELECT CartItemID, ProductID, Quantity
    #           FROM cart_item
    #          WHERE CustomerID = %s;
    #     """
    #     raw = self.db.query(select_sql, (self.customer_id,))
    #     if not isinstance(raw, list):
    #         return []
    #     rows = []
    #     for row in raw:
    #         if isinstance(row, dict):
    #             rows.append({
    #                 'CartItemID': row.get('CartItemID'),
    #                 'ProductID' : row.get('ProductID'),
    #                 'Quantity'  : row.get('Quantity')
    #             })
    #         else:
    #             cid, pid, qty = row
    #             rows.append({
    #                 'CartItemID': cid,
    #                 'ProductID' : pid,
    #                 'Quantity'  : qty
    #             })
    #     return rows

    def addToCart(self, product: Product, quantity: int):
        pid = product["id"]
        if quantity <= 0:
            return False

        for item in self._items:
            if item.getProduct()["id"] == pid:
                item.changeQuantity(item.getQuantity() + quantity)
                self._reassignIDs()
                return True

        new_item = CartItem(product, quantity)
        self._items.append(new_item)

        self._reassignIDs()
        return True
    
    def removeCartItem(self, cartItemID):
        for idx, item in enumerate(self._items):
            if item.getCartItemID() == cartItemID:
                del self._items[idx]
                self._reassignIDs()
                return True
        return False
    
    def selectCartItem(self, cartItemID):
        for item in self._items:
            if item.getCartItemID() == cartItemID:
                return item
        return None
    
    def getCartItems(self):
        return list(self._items)
    
    def place_order(self, customerID: int, items: list[CartItem], orderStatus: str, customerName: str, phoneNumber: str, shippingAddress: str, orderDate: str, totalPrice: float, db):
        insert_sql = """
            INSERT INTO orderrecord
              (CustomerID, OrderDate, OrderStatus, TotalPrice, CustomerName, PhoneNumber, ShippingAddress)
            VALUES
              (%s, %s, %s, %s, %s, %s, %s);
        """
        params = (
            customerID,
            orderDate,
            orderStatus,
            totalPrice,
            customerName,
            phoneNumber,
            shippingAddress
        )
        success = db.query(insert_sql, params)
        if not success:
            print("SQL error: could not insert new order_record.")
            return None

        last_id_rows = db.query("SELECT LAST_INSERT_ID() AS new_id;")
        if not isinstance(last_id_rows, list) or len(last_id_rows) == 0:
            print("SQL error: could not retrieve new OrderID.")
            return None

        first_row = last_id_rows[0]
        if isinstance(first_row, dict):
            new_order_id = int(first_row.get("new_id"))
        else:
            new_order_id = int(first_row[0])

        valid_pid_rows = db.query("SELECT ProductID FROM productgood;")
        valid_pids = { row["ProductID"] if isinstance(row, dict) else row[0]
                    for row in valid_pid_rows }

        for ci in items:
            pid = ci.getProduct()["id"]
            qty = ci.getQuantity()
            price_each = ci.getProduct()["price"]

            if pid not in valid_pids:
                print(f"Cannot insert orderitem: ProductID {pid} not found in productgood.")
                continue

            insert_item_sql = """
                INSERT INTO orderitem
                (OrderID, ProductID, Quantity, UnitPrice)
                VALUES
                (%s, %s, %s, %s);
            """
            item_params = (new_order_id, pid, qty, price_each)
            success2 = db.query(insert_item_sql, item_params)
            if not success2:
                print(f"Could not insert into OrderItem for ProductID={pid}.")
            else:
                print(f"Successfully inserted OrderItem for ProductID={pid}.")

        new_order = Order(
            customerId=customerID,
            items=items,
            orderStatus=OrderStatus.PENDING if orderStatus == "PENDING" else OrderStatus.PAID,
            orderID=new_order_id,
            customername=customerName,
            phoneNumber=phoneNumber,
            shippingAddress=shippingAddress
        )
        return new_order
    
    def checkout(self):
        if not self._items:
            return 0
        total = sum(item.getTotalPrice() for item in self._items)
        self._items.clear()
        self._reassignIDs()
        return total
    
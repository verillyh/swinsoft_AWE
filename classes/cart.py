from classes.itemContainer import CartItem
from classes.order import Order, OrderStatus
from classes.product import Product
from classes.invoice import Invoice

class Cart:
    def __init__(self, customerID: int):
        self.customer_id = customerID
        self._items: list[CartItem] = []

    def _reassign_id(self):
        for idx, item in enumerate(self._items, start=1):
            item.set_cart_item_id(idx)

    def clear_cart(self):
        self._items.clear()
        self._reassign_id()

    def add_to_cart(self, product: Product, quantity: int):
        pid = product.product_id
        if quantity <= 0:
            return False

        for item in self._items:
            if item.get_product()["id"] == pid:
                item.change_quantity(item.quantity + quantity)
                self._reassign_id()
                return True

        new_item = CartItem(product, quantity)
        self._items.append(new_item)
        self._reassign_id()
        return True
    
    def remove_cart_item(self, cart_item_id: int):
        for idx, item in enumerate(self._items):
            if item.get_cart_item_id() == cart_item_id:
                del self._items[idx]
                self._reassign_id()

    def toggle_cart_item_selection(self, cart_item_id: int):
        for item in self._items:
            if item.item_id == cart_item_id:
                item.is_selected = True
    
    def list_cart_items(self):
        return self._items
    
    def place_order(self, customerID: int, items: list[CartItem], orderStatus: str, customerName: str, phoneNumber: str, shippingAddress: str, orderDate: str, totalPrice: float, db):
        insert_sql = """
            INSERT INTO order_record
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

        valid_pid_rows = db.query("SELECT ProductID FROM product_good;")
        valid_pids = { row["ProductID"] if isinstance(row, dict) else row[0]
                    for row in valid_pid_rows }

        for ci in items:
            prod = ci.get_product()
            pid = prod.product_id
            qty = ci.quantity
            price_each = prod.price

            if pid not in valid_pids:
                print(f"Cannot insert orderitem: ProductID {pid} not found in productgood.")
                continue

            insert_item_sql = """
                INSERT INTO order_item
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
            customer_id=customerID,
            items=items,
            order_status=OrderStatus.PENDING if orderStatus == "PENDING" else OrderStatus.PAID,
            order_id=new_order_id,
            phone_number=phoneNumber,
            delivery_address=shippingAddress
        )

        new_invoice = Invoice(new_order.order_id, new_order.customer_id, new_order.total_cost, new_order.orderStatus)

        Cart.clear_cart(self)

        return new_invoice, new_order_id
    
import re
import sys
from classes.filter import Statisticable
from abc import abstractmethod
from classes.inboxMessage import InboxMessage
from classes.inboxInterface import InboxInterface
from classes.cart import Cart
from classes.utils import is_valid_email
from classes.statistic import Statistic
from classes.invoice import Invoice
from classes.itemContainer import OrderItem
from classes.order import Order, OrderStatus
from classes.product import Product
from classes.payment import Payment

class Account(InboxInterface):
    def __init__(self, privilege: int, email: str, address: str, username: str, password_hashed: str, account_id: int = None):
        self.account_id = account_id
        self.privilege = privilege
        self.email = email
        self.address = address
        self.username = username
        self._password_hashed = password_hashed
        self._inbox: list[InboxMessage] = [] 

    @property
    def password(self):
        raise AttributeError("Cannot read password.")
    
    @password.setter
    def password(self, value: str):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self._password_hashed = Account._hash_password(value)

    @staticmethod
    def _hash_password(password: str):
        return f"hashed_{password}"

    @classmethod
    @abstractmethod
    def signup(cls, privilege: int, email: str, address: str, username: str, password: str, db):
        email = email.strip()
        address = address.strip()
        username = username.strip()
        password = password.strip()

        if not is_valid_email(email):
            print("Invalid email format.")
            return False
        
        password_hashed = cls._hash_password(password)
        insert_sql = """
            INSERT INTO account
              (AccountType, Email, StreetAddress, UserName, Password)
            VALUES
              (%s, %s, %s, %s, %s);
        """
        params = (privilege, email, address, username, password_hashed)
        success = db.query(insert_sql, params)
        if not success:
            print("SQL error on inserting new account.")
            return False
        
        last_id_sql = "SELECT LAST_INSERT_ID();"
        raw = db.query(last_id_sql)
        if not isinstance(raw, list) or len(raw) == 0:
            print("Error: could not retrieve last insert ID.")
            return False
        
        new_account_id = raw[0]
        
        newUser = cls(
            privilege,
            email,
            address,
            username,
            password_hashed,
            account_id=new_account_id
        )
        return newUser
    
    @classmethod
    def login(cls, email: str, password: str, db):
        email = email.strip()
        password = password.strip()
        password_hashed = cls._hash_password(password)

        select_query = """
            SELECT
            AccountID,
            UserName,
            Password,
            StreetAddress,
            AccountType,
            Email
            FROM account
            WHERE Email = %s AND Password = %s;
        """
        params = (email, password_hashed)

        result = db.query(select_query, params)
        if not isinstance(result, list) or len(result) == 0:
            return None

        row = result[0]
        db_account_id       = row["AccountID"]
        db_username         = row["UserName"]
        db_password_hashed  = row["Password"]
        db_street           = row["StreetAddress"]
        db_privilege        = row["AccountType"]
        db_email            = row["Email"]

        if db_privilege == "OWNER":
            Subclass = OwnerAccount
        elif db_privilege == "STAFF":
            Subclass = StaffAccount
        else:
            Subclass = CustomerAccount

        user = Subclass(
            db_privilege,      
            db_email,              
            db_street,            
            db_username,           
            db_password_hashed,   
            db_account_id
        )

        return user
        
    def modify_account_detail(self, field: str, new_value: str, db):
        field = field.strip()
        if field not in ["email", "username", "address", "password"]:
            print(f"Cannot modify '{field}', not allowed or read-only.")
            return False
        
        new_value = new_value.strip()
        if field == "email":
            if not is_valid_email(new_value):
                print("Invalid email format.")
                return False
            update_field = f"Email = '{new_value}'"
            self._email = new_value

        elif field == "username":
            if len(new_value) == 0:
                print("Username cannot be empty.")
                return False
            update_field = f"UserName = '{new_value}'"
            self._username = new_value

        elif field == "address":
            update_field = f"StreetAddress = '{new_value}'"
            self._address = new_value

        else:
            if len(new_value) < 8:
                print("Password must be at least 8 characters.")
                return False
            password_hashed = Account._hash_password(new_value)
            update_field = f"Password = '{password_hashed}'"
            self._password_hashed = password_hashed

        update_query = (
            f"UPDATE account"
            f"SET {update_field} "
            f"WHERE AccountID = {self.account_id};"
        )
        db.query(update_query)
        print("Account detail modified.")
        return True
    
    def __row_to_message(self, row: tuple):
        (message_id, sender, content) = row
        return InboxMessage(message_id, self.account_id, sender, content, "FALSE")
    
    def create_inbox_message(message: str, db):
        insert_sql = """
        INSERT INTO Inbox_Message (RecipientID, Sender, Content)
         VALUES
         (%s, %s, %s);
        """
        params = (message, message, message)
        db.query(insert_sql, params)
    
    def open_inbox(self, db):
        select_sql = """
        SELECT AccountType
         FROM Account
         WHERE AccountID = %s;
        """
        params = (self.account_id)
        account_type = db.query(select_sql, params) 

        if account_type == "STAFF":
            select_sql1 = """
            SELECT MessageID, Sender, Content, CreatedAt
             FROM Inbox_Message;
            """
            raw = db.query(select_sql1,)
        else: 
            select_sql2 = """
            SELECT MessageID, Sender, Content, CreatedAt
             FROM Inbox_Message
             WHERE RecipientID = %s;
            """
            params2 = (self.account_id)
            raw = db.query(select_sql2, params2)

        messages = []
        for row in raw:
            if isinstance(row, tuple) and len(row) == 4:
                tup = row
            elif isinstance(row, dict):
                try:
                    tup = (
                        row["MessageID"],
                        row["Sender"],
                        row["Content"],
                        row["CreatedAt"]
                    )
                except KeyError:
                    continue
            else:
                continue
            message = self.__row_to_message(tup, db)
            messages.append(message)

        if not messages:
            return "No message available.\n"
        
        lines = []
        for msg in messages:
            lines.append(str(msg))
            lines.append("-" * 40)

        return "\n".join(lines)
    
    def show_inbox_message(self):
        if not self._inbox:
            print("Inbox is empty.")
            return

        for msg in self._inbox:
            msg.show_inbox_message() 

    def get_invoice_history(self, db):
        select_invoices_sql = """
            SELECT
            InvoiceID,
            OrderID,
            CustomerID,
            AmountDue,
            InvoiceStatus
            FROM Invoice
            WHERE CustomerID = %s
            ORDER BY InvoiceID DESC;
        """
        invoice_params = (self.account_id,) 
        raw_invoices = db.query(select_invoices_sql, invoice_params)

        if not raw_invoices or len(raw_invoices) == 0:
            return "No invoices found for this customer.\n"

        output_lines: list[str] = []

        for inv_row in raw_invoices:
            if isinstance(inv_row, dict):
                invoice_id     = inv_row["InvoiceID"]
                order_id       = inv_row["OrderID"]
                customer_id    = inv_row["CustomerID"]
                amount_due     = float(inv_row["AmountDue"])
                invoice_status = inv_row["InvoiceStatus"]
            else:
                invoice_id, order_id, customer_id, amount_due, invoice_status = inv_row

            output_lines.append(f"Invoice #{invoice_id}")
            output_lines.append(f"  Order ID    : {order_id}")
            output_lines.append(f"  Customer ID : {customer_id}")
            output_lines.append(f"  Amount Due  : ${amount_due:.2f}")
            output_lines.append(f"  Status      : {invoice_status}")
            output_lines.append("  Items:")

            select_items_sql = """
                SELECT
                oi.ProductID,
                pg.Name           AS ProductName,
                pg.UnitPrice      AS ProductPrice,
                oi.Quantity       AS ItemQuantity
                FROM order_item oi
                JOIN product_good pg ON oi.ProductID = pg.ProductID
                WHERE oi.OrderID = %s
                ORDER BY oi.ProductID;
            """
            item_params = (order_id,)
            raw_items = db.query(select_items_sql, item_params)

            order_items: list[OrderItem] = []
            if not raw_items or len(raw_items) == 0:
                output_lines.append("    (No items found for this invoice.)")
            else:
                output_lines.append("    ProductID | ProductName       | Qty | UnitPrice | LineTotal")
                output_lines.append("    " + "-" * 60)

                for item_row in raw_items:
                    if isinstance(item_row, dict):
                        pid        = item_row["ProductID"]
                        pname      = item_row["ProductName"]
                        pprice     = float(item_row["ProductPrice"])
                        qty        = int(item_row["ItemQuantity"])
                    else:
                        pid, pname, pprice, qty = item_row

                    prod = Product(
                        productID   = pid,
                        name        = pname,
                        description = "",     
                        price       = pprice,
                        quantity    = 0,     
                        category    = None,   
                        brand       = None   
                    )

                    line_total = qty * pprice
                    oi = OrderItem(prod, qty, line_total)
                    order_items.append(oi)

                    output_lines.append(
                        f"    {pid:<9} | {pname:<18} | {qty:>3} | "
                        f"${pprice:>8.2f} | ${line_total:>8.2f}"
                    )

            order = Order(
                customer_id  = customer_id,
                order_id     = order_id,
                items        = order_items,
                order_status = OrderStatus.PAID,
                phone_number= "",
                delivery_address= ""
            )
            
            is_paid_flag = (invoice_status.upper() == "PAID")
            invoice = Invoice(
                customer_id    = customer_id,
                amountDue      = amount_due,
                order_id = order_id,
                invoiceID      = invoice_id,
                invoice_status         = is_paid_flag,
                order_contents = order
            )

            output_lines.append(str(invoice))
            output_lines.append("-" * 80)

        return "\n".join(output_lines)

    def get_order_history():
        pass

    def __row_to_product(self, row: list[tuple]):
        products = []
        for it in row:

            (invoice_id, customer_id, invoice_amount_due, invoice_status, order_id, order_date, order_status, order_item_id, product_id, product_name, quantity, unit_price, category, brand, description) = it
            products.append(Product(name=product_name, description=description, price=unit_price, quantity=quantity, category=category, brand=brand, productID=product_id))
        return products

    def __row_to_order_item(self, row: list[tuple]):
        item = []
        for it in row:
            (invoice_id, customer_id, invoice_amount_due, invoice_status, order_id, order_date, order_status, order_item_id, product_id, product_name, quantity, unit_price, category, brand, description) = it
            item.append(OrderItem(product=self.__row_to_product([it]), quantity=quantity, total_price=unit_price*quantity))
        return item

    def __row_to_order(self, row: list[tuple]):
        item = []
        for it in row:
            (invoice_id, customer_id, invoice_amount_due, invoice_status, order_id, order_date, order_status, order_item_id, product_id, product_name, quantity, unit_price, category, brand, description) = it
            item.append(Order(customer_id=customer_id, items=self.__row_to_order_item([it]), order_status=OrderStatus.PAID, order_id=order_id, phone_number="", delivery_address=""))
        return item 

    def __row_to_invoice(self, row: list[tuple], db):
        item = []
        for it in row:
            (invoice_id, customer_id, invoice_amount_due, invoice_status, order_id, order_date, order_status, order_item_id, product_id, product_name, quantity, unit_price, category, brand, description) = it
            item.append(Invoice(customer_id=customer_id, amountDue=invoice_amount_due, order_id=order_id,invoiceID=invoice_id, invoice_status=invoice_status, order_contents=self.__row_to_order([it])))
        return item
    
    def get_receipt_history(self, db):
        select_sql = """
        SELECT
            inv.InvoiceID        AS invoice_id,
            inv.CustomerID       AS customer_id,
            inv.AmountDue        AS invoice_amount_due,
            inv.InvoiceStatus    AS invoice_status,

            ordr.OrderID         AS order_id,
            ordr.OrderDate       AS order_date,
            ordr.OrderStatus     AS order_status,

            oi.OrderItemID       AS order_item_id,
            oi.ProductID         AS product_id,
            pg.Name              AS product_name,
            oi.Quantity          AS quantity,
            oi.UnitPrice         AS unit_price,
            pg.CategoryID        AS category,
            pg.BrandID           AS brand,
            pg.Description       AS description

            FROM Invoice inv
            JOIN order_record ordr
            ON inv.OrderID = ordr.OrderID
            JOIN order_item oi
            ON ordr.OrderID = oi.OrderID
            JOIN product_good pg
            ON oi.ProductID = pg.ProductID

            WHERE inv.CustomerID = %s
            ORDER BY inv.InvoiceID DESC, oi.ProductID;
        """
        params = (self.account_id)
        raw = db.query(select_sql, params)

        invoices = []
        orders = []
        tups = []
        for row in raw:
            if isinstance(row, tuple) and len(row) == 15:
                tup = row
            elif isinstance(row, dict):
                try:
                    tup = (
                        row["invoice_id"],
                        row["customer_id"],
                        row["invoice_amount_due"],
                        row["invoice_status"],
                        row["order_id"],
                        row["order_date"],
                        row["order_status"],
                        row["order_item_id"],
                        row["product_id"],
                        row["product_name"],
                        row["quantity"],
                        row["unit_price"],
                        row["category"],
                        row["brand"],
                        row["description"]
                    )
                    tups.append(tup)
                except KeyError:
                    continue
            else:
                continue
        invoices = self.__row_to_invoice(tups, db)
        # invoices.append(invoice_obj)

        orders = self.__row_to_order(tups)
        # orders.append(orders_obj)
        receipts = []
        for invoice in invoices:
            # print(invoice)
            new_receipt = Payment().generate_receipt(invoice)
            receipts.append(new_receipt)
            # print(new_receipt)
        return receipts
    
class OwnerAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None):
        super().__init__(1, email, address, username, password, account_id)
        self._generatedStatistics : list[Statistic] = []

    @classmethod
    def signup(cls, email: str, address: str, username: str, password: str, db):
        return super().signup(1, email, address, username, password, db)
    
    def add_staff(self, email: str, address: str, username: str, password: str, db):
        new_staff = StaffAccount.signup(email, address, username, password, db)
        if isinstance(new_staff, Account):
            print("Staff account created in database.")
            return True
        else:
            print("Failed to create staff account.")
            return False
    
    def remove_staff(self, staffID: int, db):
        try:
            pid = int(staffID)
        except ValueError:
            return False

        delete_sql = f"DELETE FROM account WHERE AccountID = {pid} AND AccountType = 'STAFF';"
        db.query(delete_sql)
        return True
    
    def list_staff(self, db):
        rows = db.query("SELECT AccountID, Email, StreetAddress, UserName FROM account WHERE AccountType = 'STAFF';")
        staff_list = []
        for row in rows:
            staff_str = (
                f"ID: {row['AccountID']} | "
                f"Email: {row['Email']} | "
                f"Address: {row['StreetAddress']} | "
                f"Username: {row['UserName']}"
            )
            staff_list.append(staff_str)

        return staff_list

class StaffAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None):
        super().__init__(2, email, address, username, password, account_id)

    @classmethod
    def signup(cls, email: str, address: str, username: str, password: str, db):
        return super().signup(2, email, address, username, password, db)

    # discussion
    @classmethod
    def fetch_all_staff(cls, db):
        rows = db.query("SELECT AccountID, Email, StreetAddress, UserName, Password FROM account WHERE AccountType = 'STAFF';")
        staff_list = []
        for row in rows:
            staff_list.append(cls(
                row["Email"],
                row["StreetAddress"],
                row["UserName"],
                row["Password"],
                row["AccountID"]
            ))
        return staff_list

class CustomerAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None):
        super().__init__(3, email, address, username, password, account_id)
        self.cart = Cart(self.account_id)

    @classmethod
    def signup(cls, email: str, address: str, username: str, password: str, db):
        return super().signup(3, email, address, username, password, db)

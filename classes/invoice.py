class Invoice:
    def __init__(self, invoiceID: int, orderID: int, customerID: int, amountDue: float, status: str):
        self.invoiceID = invoiceID
        self.orderID = orderID
        self.customerID = customerID
        self.amountDue = amountDue
        self.status = status

    @classmethod
    def create_invoice(cls, db, orderID: int, customerID: int, amountDue: float, status: str):
        insert_sql = """
            INSERT INTO invoice
              (OrderID, CustomerID, AmountDue, InvoiceStatus)
            VALUES
              (%s, %s, %s, %s);
        """
        params = (orderID, customerID, amountDue, status)
        db.query(insert_sql, params)

        last_id_sql = "SELECT LAST_INSERT_ID();"
        raw = db.query(last_id_sql)
        if not isinstance(raw, list) or len(raw) == 0:
            raise Exception("Could not retrieve last insert ID for Invoice.")

        row0 = raw[0]
        if isinstance(row0, tuple):
            inv_id = row0[0]
        elif isinstance(row0, dict):
            inv_id = list(row0.values())[0]
        else:
            raise Exception("Unexpected return type for LAST_INSERT_ID.")

        return cls(inv_id, orderID, customerID, amountDue, status)

    @classmethod
    def fetch_by_order(cls, db, orderID: int):
        select_sql = """
            SELECT
              InvoiceID,
              CustomerID,
              AmountDue,
              InvoiceStatus
            FROM Invoice
            WHERE OrderID = %s;
        """
        rows = db.query(select_sql, (orderID,))
        if not rows:
            return None

        row = rows[0]
        return cls(
            row["InvoiceID"],
            orderID,
            row["CustomerID"],
            float(row["AmountDue"]),
            row["InvoiceStatus"],
        )

    def update_status_db(self, db, new_status: str):
        update_sql = """
            UPDATE Invoice
            SET InvoiceStatus = %s
            WHERE InvoiceID = %s;
        """
        db.query(update_sql, (new_status, self.invoiceID))
        self.status = new_status

    def __str__(self):
        return (
            f"Invoice ID   : {self.invoiceID}\n"
            f"Order ID     : {self.orderID}\n"
            f"Customer ID  : {self.customerID}\n"
            f"Amount Due   : ${self.amountDue:.2f}\n"
            f"Status       : {self.status}\n"
        )

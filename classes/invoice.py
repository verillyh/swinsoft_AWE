from classes.payment import Payment
from classes.receipt import Receipt
from classes.order import Order, OrderStatus

class Invoice:
    def __init__(self, customer_id: int, amountDue: float, order_id: int, invoiceID: int = None, *, invoice_status: False, order_contents: Order):
        self.customer_id = customer_id
        self.invoice_id = invoiceID
        self.amountDue = amountDue
        self.is_paid = invoice_status
        self.order_id = order_id
        self.order_contents = order_contents

    def __row_to_order(row: tuple):
        (order_id, customer_id, order_date, order_status, total_price, customer_name, phone_number, shipping_address) = row

        return Order(customer_id=customer_id, items="", order_status=OrderStatus.PENDING, order_id=order_id, phone_number=phone_number, delivery_address=shipping_address, total_cost=total_price)

    def get_invoice(id, db):
        select_sql = """
            SELECT *
             FROM invoice
             WHERE InvoiceID = %s AND InvoiceStatus = "PENDING"
             LIMIT 1;
        """
        params = (id,)
        raw = db.query(select_sql, params)
        
        try:
            row = raw[0]
        except:
            print("The invoice is already paid.")
            return

        if isinstance(row, dict):
            try:
                invoice_id        = row["InvoiceID"]
                order_id           = row["OrderID"]
                customer_id    = row["CustomerID"]
                amount_due     = row["AmountDue"]
                invoice_status     = row["InvoiceStatus"]
            except KeyError:
                raise Exception("not dict")
            
            select_sql = """
            SELECT *
             FROM order_record
             WHERE OrderID = %s
            """
            params = (order_id)
            row = db.query(select_sql, params)
            row = row[0]
            if isinstance(row, tuple) and len(row) == 8:
                tup = row
            elif isinstance(row, dict):
                try:
                    tup = (
                        row["OrderID"],
                        row["CustomerID"],
                        row["OrderDate"],
                        row["OrderStatus"],
                        row["TotalPrice"],
                        row["CustomerName"],
                        row["PhoneNumber"],
                        row["ShippingAddress"],
                    )
                except KeyError:
                    raise KeyError("Key error in getting invoice details")
            order_obj = Invoice.__row_to_order(tup)

            return Invoice(
                customer_id=customer_id,
                amountDue=amount_due,
                order_id=order_id,
                invoiceID=invoice_id,
                invoice_status=invoice_status,
                order_contents=order_obj
            )

    def pay_invoice(self, db, cardholder_name, card_number, expiry_month, expiry_year, cvv_int, invoice_id, invoice):
        Payment().request_payment_from_vendor(
            card_number,
            expiry_month,
            expiry_year,
            cvv_int,
            invoice
        )
        print(self.invoice_id)
        print(invoice.order_id)

        update_sql = """
            UPDATE invoice
             SET InvoiceStatus = "PAID"
             WHERE InvoiceID = %s;
        """
        db.query(update_sql, (self.invoice_id))

        update_sql1 = """
            UPDATE order_record
             SET OrderStatus = "PAID"
             WHERE OrderID = %s;
        """
        db.query(update_sql1, (invoice.order_id))

        new_receipt = Receipt(invoice)
        return new_receipt

    def __str__(self):
        return (
            f"Invoice ID   : {self.invoice_id}\n"
            f"Order ID   : {self.order_id}\n"
            f"Customer ID   : {self.customer_id}\n"
            f"Amount Due   : ${self.amountDue:.2f}\n"
            f"Status       : {self.is_paid}\n"
        )

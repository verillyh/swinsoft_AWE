import random
import string
from classes.receipt import Receipt


class Payment:
    def request_payment_from_vendor(self, cardNumber: str, monthExpiry: int, yearExpiry: int, cvv: int, invoice):
        print("Requesting payment from vendor...")
        transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print(f"Transaction ID: {transaction_id}")
        self.__validate_transaction(transaction_id)
    
    def __validate_transaction(self, transaction_id: str):
        print(f"Validating transaction {transaction_id}...")
        return True

    def generate_receipt(self, invoice):
        print("Generating receipt...")
        receipt_id = random.randint(1000, 9999)
        receipt = Receipt(invoice)
        return receipt
    #     order_id = invoice.order_id
    #     total = invoice.amountDue
    #     items = [(item.product.name, item.quantity, item.product.price) for item in invoice.order_contents.items]
    
    #     item_lines = "\n".join([f"  - {name} x{qty} @ ${price:.2f}" for name, qty, price in items])
    
    #     return (
    #         f"# =================================================== \n {'RECEIPT' .center(50)} \n# =================================================== \n"
    #         f"Receipt ID: {receipt_id}\n"
    #         f"Order ID: {order_id}\n"
    #         f"Items:\n{item_lines}\n"
    #         f"Total: ${total}\n"
    # )

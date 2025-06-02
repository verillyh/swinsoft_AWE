import random
import string

class Payment:
    def requestPaymentFromVendor(self, cardNumber: str, monthExpiry: int, yearExpiry: int, cvv: int) -> str:
        print("Requesting payment from vendor...")
        transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print(f"Transaction ID: {transaction_id}")
        return transaction_id    
    def validateTransaction(self, transaction_id: str) -> bool:
        print(f"Validating transaction {transaction_id}...")
        return True

    def generateReceipt(self, order):
        print("Generating receipt...")
        receipt_id = random.randint(1000, 9999)
        order_id = order.getOrderId()
        total = order.getTotalCost()
        items = [(item.getProduct()['name'], item.getQuantity()) for item in order.getItems()]
    
        item_lines = "\n".join([f"  - {name} x{qty}" for name, qty in items])
    
        return (
            f"# =================================================== \n {'RECEIPT' .center(50)} \n# =================================================== \n"
            f"Receipt ID: {receipt_id}\n"
            f"Order ID: {order_id}\n"
            f"Items:\n{item_lines}\n"
            f"Total: ${total}\n"
    )

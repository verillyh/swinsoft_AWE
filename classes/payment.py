import random
import string
from invoice import Invoice
from receipt import Receipt

class Payment:
    def requestPaymentFromVendor(self, cardNumber: str, monthExpiry: int, yearExpiry: int, cvv: int) -> str:
        print("Requesting payment from vendor...")
        transaction_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print(f"Transaction ID: {transaction_id}")
        return transaction_id    
    def validateTransaction(self, transaction_id: str) -> bool:
        print(f"Validating transaction {transaction_id}...")
        return True

    def generateReceipt(self, invoice: Invoice):
        if not invoice.isPaid:
            print("Error: Cannot generate receipt for unpaid invoice.")
            return None
        return Receipt(invoice)

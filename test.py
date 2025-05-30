from classes.cart import Cart
from classes.cartItem import CartItem
from classes.order import Order, OrderStatus
from classes.payment import Payment

# 1. Sample Products
product1 = {'id': 101, 'name': 'Laptop', 'price': 1200}
product2 = {'id': 102, 'name': 'Mouse', 'price': 25}

# 2. Create a cart and add products
cart = Cart()
cart.addToCart(product1, 1)
cart.addToCart(product2, 2)


print("🛒 Cart Contents:")
print(cart.listProductsInCart())

total = cart.checkout()
print(f"\n💰 Checkout Total: ${total}")

cart.addToCart(product1, 1)
cart.addToCart(product2, 2)
order = Order(customerId=1, items=cart._Cart__cartItems)

# 6. Notify staff and change status
order.notifyStaff()
order.updateStatus(1001, OrderStatus.PAID)

# 7. Process payment
payment = Payment()
transaction_id = payment.requestPaymentFromVendor("1234567890123456", 12, 2025, 123)

if payment.validateTransaction(transaction_id):
    receipt = payment.generateReceipt(order)
    print("\n Receipt:")
    print(receipt)
else:
    print("\n Payment failed.")

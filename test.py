from classes.cart import Cart
<<<<<<< Updated upstream

product_1 = {'id': 101, 'name': 'Product_1', 'price': 1500}
product_2 = {'id': 104, 'name': 'Product_4', 'price': 800}

def main():
    print("=== SHOPPING CART DEMO ===\n")

    cart = Cart()
    cart.customer_id = 123  

    cart.addToCart(product_1, 1)
    cart.addToCart(product_2, 2)

    print(">>> CART CONTENTS\n")
    cart.cartUI()

    print("\n>>> STARTING CHECKOUT...\n")
    cart.checkoutUI()
=======
from classes.uI import ClassUI  # Make sure your file is named `uI.py`, not `ui.py` or `UI.py`

# Sample product data
product1 = {'id': 1, 'name': 'Wireless Mouse', 'price': 25.99}
product2 = {'id': 2, 'name': 'Keyboard', 'price': 45.50}
product3 = {'id': 3, 'name': 'USB-C Cable', 'price': 12.00}

def main():
    print("=== CHECKOUT SYSTEM TEST ===")
    
    # Create cart and UI with customer ID
    cart = Cart()
    cart.customer_id = 101
    ui = ClassUI(cart, customer_id=101)

    # Add sample items to cart
    cart.addToCart(product1, 2)
    cart.addToCart(product2, 1)
    cart.addToCart(product3, 3)

    # Call the checkout UI to run the full flow
    ui.checkoutUI()
>>>>>>> Stashed changes

if __name__ == "__main__":
    main()

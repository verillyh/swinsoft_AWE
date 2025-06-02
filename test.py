from classes.cart import Cart

# Sample products
product_1 = {'id': 101, 'name': 'Product_1', 'price': 1500}
product_2 = {'id': 104, 'name': 'Product_4', 'price': 800}

def main():
    print("=== SHOPPING CART DEMO ===\n")

    # Create cart and simulate customer
    cart = Cart()
    cart.customer_id = 123  # inject required attribute

    # Add products
    cart.addToCart(product_1, 1)
    cart.addToCart(product_2, 2)
    
    # Display cart
    print(">>> CART CONTENTS\n")
    cart.cartUI()

    # Proceed to checkout
    print("\n>>> STARTING CHECKOUT...\n")
    cart.checkoutUI()

if __name__ == "__main__":
    main()

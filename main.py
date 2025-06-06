import os
import sys
import re

from classes.account import Account, ownerAccount, staffAccount, customerAccount
from classes.productCatalogue import ProductCatalogue
from classes.product import Brand, Category
from classes.cart import Cart
from classes.database import Database
from classes.order import Order, OrderStatus
from classes.payment import Payment
from classes.itemContainer import CartItem as CI
from classes.inboxMessage import InboxMessage
from classes.invoice import Invoice
from datetime import datetime

# Database connection
_db = Database("awe_electronics")
_db.connect("awe_electronics")

Brand = Brand(_db)
Category = Category(_db)

GUEST_CART = Cart(customerID=None)
CURRENT_USER: Account | None = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def login_ui():
    global CURRENT_USER
    clear_screen()
    print("# ==================================================")
    print("                    LOGIN                          ")
    print("# ==================================================\n")

    email = input("Enter email: ").strip()
    password = input("Enter password: ").strip()

    if not email or not password:
        print("\nEmail or password cannot be empty. Try again.")
        input("\nPress Enter to continue…")
        return False

    user = Account.login(email, password, _db)
    if user:
        CURRENT_USER = user
        print("\nLogin successful.")
    else:
        print("\nLogin failed.")
    input("\nPress Enter to continue…")

def signup_ui():
    global CURRENT_USER
    clear_screen()
    print("# ==================================================")
    print("                CREATE NEW ACCOUNT                 ")
    print("# ==================================================\n")

    email         = input("Email         : ").strip()
    streetAddress = input("Street Address: ").strip()
    username      = input("Username      : ").strip()
    password      = input("Password (≥8) : ").strip()

    new_user = customerAccount.signup(email, streetAddress, username, password, _db)
    if not new_user:
        input("\nPress Enter to continue…")
        return False
    else:
        CURRENT_USER = new_user
        clear_screen()
        print(f"Account created! Logged in as '{new_user.username}'.")

    input("\nPress Enter to continue…")
    return True

def product_ui(productCatalogue: ProductCatalogue):
    all_products = productCatalogue.fetch_all_products(_db)
    if len(all_products) == 0:
        print("No products available.\n")
    else:
        for prod in all_products:
            print(prod)        
            print("-" * 40)

def browse_catalogue(productCatalogue: ProductCatalogue):
    clear_screen()
    print("# ==================================================")
    print("                PRODUCT CATALOGUE                   ")
    print("# ==================================================\n")

    product_ui(productCatalogue)

    input("Press Enter to return to the menu…")

def search_product(productCatalogue: ProductCatalogue):
    clear_screen()
    print("# ==================================================")
    print("                SEARCH PRODUCT                      ")
    print("# ==================================================\n")
    keyword = input("Enter product name or keyword: ").strip()
    results = productCatalogue.fetch_product_detail(keyword, _db)

    if not results:
        print("\nNo products match this keyword.\n")
    else:
        print(f"\nFound {len(results)} matching product(s):\n")
        for prod in results:
            print(prod)
            print("-" * 40)

    input("\nPress Enter to return to the menu…")

def add_product_to_cart(productCatalogue: ProductCatalogue):
    clear_screen()
    print("# ==================================================")
    print("             ADD PRODUCT TO CART                    ")
    print("# ==================================================\n")

    product_ui(productCatalogue)

    try:
        choice = int(input("\nEnter product ID to add to cart: ").strip())
    except ValueError:
        print("Invalid ID. Returning to previous menu.")
        input("\nPress Enter to continue…")
        return

    product_obj = productCatalogue.fetch_product_by_id(choice, _db)
    if not product_obj:
        print("\nNo product with this ID.")
        input("\nPress Enter to continue…")
        return

    try:
        amount = int(input("Enter quantity: ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("Quantity must be a positive integer.")
        input("\nPress Enter to continue…")
        return
    
    if amount > product_obj.quantity:
        print(f"\nCannot add {amount} '{product_obj.name}' to cart: only {product_obj.quantity} in stock.")
        input("\nPress Enter to continue...")
        return 

    product_dict = {
        "id": product_obj.id,
        "name": product_obj.name,
        "price": product_obj.price
    }

    if CURRENT_USER is None:
        GUEST_CART.add_to_cart(product_dict, amount)
    else:
        CURRENT_USER.cart.add_to_cart(product_dict, amount)

    print(f"\nAdded {amount} × '{product_obj.name}' to your cart.")
    input("\nPress Enter to continue…")

def checkout_ui(cart):
    if CURRENT_USER is None or not hasattr(CURRENT_USER, "accountID"):
        print("\nYou must be logged in to place an order.")
        input("\nPress Enter to return to the menu…")
        return
    
    clear_screen()
    print("#" + "=" * 50)
    print(f"{'CHECKOUT':^52}")
    print("#" + "=" * 50 + "\n")

    items = cart.get_cart_items()
    if not items:
        print("Your cart is empty; nothing to checkout.\n")
        input("Press Enter to return to the menu…")
        return

    grand_total = 0.0
    for item in items:
        prod       = item.get_product()
        name       = prod["name"]
        unit_price = prod["price"]
        qty        = item.get_quantity()
        line_total = unit_price * qty
        grand_total += line_total
        print(f"{name} × {qty} @ ${unit_price:.2f} = ${line_total:.2f}")
        print("-" * 40)

    print(f"\nGrand Total: ${grand_total:.2f}\n")

    print("#" + "=" * 50)
    print(f"{'ENTER SHIPPING DETAILS':^52}")
    print("#" + "=" * 50 + "\n")
    phone_number = input("Phone Number      : ").strip()
    delivery_address = input("Delivery Address  : ").strip()

    if  not phone_number or not delivery_address:
        print("\nDelivery details cannot be blank. Aborting checkout.")
        input("\nPress Enter to return to the menu…")
        return

    print("\nShipping info recorded successfully.\n")

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_order = cart.place_order(
        customerID = CURRENT_USER.accountID,     
        items = cart.get_cart_items(),        
        orderStatus = "PENDING",                   
        phoneNumber = phone_number,               
        shippingAddress = delivery_address,                    
        orderDate = order_date,                 
        totalPrice = grand_total,                
        db = _db                         
    )

    choice = input("[1] Pay and complete checkout   [0] Cancel\n\nEnter choice: ").strip()
    if choice != "1":
        print("Checkout cancelled.")
        new_order.orderStatus = "CANCELLED"
        input("\nPress Enter to return to the menu…")
        return

    clear_screen()
    print("#" + "=" * 50)
    print(f"{'ENTER PAYMENT DETAILS':^52}")
    print("#" + "=" * 50 + "\n")
    cardholder_name = input("Cardholder Name   : ").strip()
    card_number     = input("Card Number       : ").strip()
    expiry          = input("Expiry (MM/YY)    : ").strip()
    cvv             = input("CVV               : ").strip()

    try:
        expiry_month, expiry_year = map(int, expiry.split("/"))
        cvv_int = int(cvv)
    except ValueError:
        print("\nInvalid expiry or CVV format. Aborting payment.")
        input("\nPress Enter to return to the menu…")
        return

    payment = Payment()
    transaction_id = payment.request_payment_from_vendor(
        card_number,
        expiry_month,
        expiry_year,
        cvv_int
    )
    if not payment.validate_transaction(transaction_id):
        print("\nPayment failed. Transaction invalid.")
        input("\nPress Enter to return to the menu…")
        return

    items = cart.get_cart_items()
    for item in items:
        prod = item.get_product()
        prod_id = prod["id"]
        qty_ordered = item.get_quantity()
 
        update_sql = """
            UPDATE product_good
               SET StockQuantity = StockQuantity - %s
             WHERE ProductID = %s;
        """
        _db.query(update_sql, (qty_ordered, prod_id))

    staff_message_content = f"Order {new_order.orderID} placed with status {new_order.orderStatus.value}."

    sql_staff_ids = """
        SELECT AccountID, UserName
          FROM account
        WHERE AccountType = "STAFF";
    """
    staff_rows = _db.query(sql_staff_ids)
    if isinstance(staff_rows, list):
        for row in staff_rows:

            if isinstance(row, dict):
                staff_id   = row["AccountID"]
                staff_name = row["UserName"]
            else:
                staff_id, staff_name = row

            InboxMessage.create(
                recipientID=staff_id,
                sender=CURRENT_USER.username,
                content=staff_message_content,
                db=_db
            )

    customer_notice = f"Your order {new_order.orderID} has been placed (status: {new_order.orderStatus.value})."
    InboxMessage.create(
        recipientID=CURRENT_USER.accountID,
        sender="SYSTEM",
        content=customer_notice,
        db=_db
    )

    invoice = Invoice.create_invoice(_db, new_order.orderID, CURRENT_USER.accountID, grand_total, "PAID")
    receipt_str = str(invoice)
    InboxMessage.create(
        recipientID=CURRENT_USER.accountID,
        sender="SYSTEM",
        content=receipt_str,
        db=_db
    )

    cart.clear_cart()
    return

def view_cart():
    clear_screen()
    print("#" + "=" * 50)
    print("                  YOUR CART                        ")
    print("#" + "=" * 50 + "\n")

    if CURRENT_USER is None:
        cart = GUEST_CART
        print("** You are viewing as a guest. You must log in or sign up to check out. **\n")
    else:
        cart = CURRENT_USER.cart

    if not cart.get_cart_items():
        print("Your cart is currently empty.\n")
        input("Press Enter to return to the menu…")
        return

    while True:
        clear_screen()
        items = cart.get_cart_items()

        if not items:
            print("Your cart is now empty.\n")
            input("Press Enter to return to the menu…")
            return

        grand_total = 0.0
        for item in items:
            cartItemID = item.get_cart_item_id()      
            prod = item.get_product()
            prod_id = prod["id"]                      
            name = prod["name"]
            unit_price = prod["price"]
            qty = item.get_quantity()
            line_total = unit_price * qty
            grand_total += line_total
            print(f"[{cartItemID}] {name} (PID {prod_id}) – ${unit_price:.2f} × {qty} = ${line_total:.2f}")
            print("-" * 40)

        print(f"\nGrand Total: ${grand_total:.2f}\n")
        print("[1] Remove Item")
        print("[2] Update Quantity")
        print("[3] Proceed to Checkout")
        print("[0] Return to Main Menu")
        print("[X] Return to Previous Page")

        choice = input("\nEnter choice: ").strip().upper()
        if choice == "1":
            try:
                cid = int(input("\nEnter the **CartItemID** to remove: ").strip())
            except ValueError:
                print("Invalid input. CartItemID must be an integer.")
                input("\nPress Enter to continue…")
                continue

            success = cart.remove_cart_item(cid)
            if success:
                print(f"Item #{cid} removed successfully.")
            else:
                print(f"CartItemID {cid} not found in your cart.")
            input("\nPress Enter to continue…")
            continue

        elif choice == "2":
            try:
                cid = int(input("\nEnter the **CartItemID** to update: ").strip())
                new_qty = int(input("Enter the new quantity: ").strip())
                if new_qty <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input. Please enter a valid CartItemID and a positive integer quantity.")
                input("\nPress Enter to continue…")
                continue

            found_item = None
            for item in items:
                if item.get_cart_item_id() == cid:
                    item.change_quantity(new_qty)
                    found_item = item
                    break

            if not found_item:
                print(f"CartItemID {cid} not found in your cart.")
            else:
                print(f"Quantity for CartItem #{cid} updated to {new_qty}.")

            input("\nPress Enter to continue…")
            continue

        elif choice == "3":
            if CURRENT_USER is None:
                print("\nYou must log in or create an account to check out.")
                login_signup_menu()
                input("\nPress Enter to continue…")
                return

            checkout_ui(cart)

        elif choice == "0":
            return

        elif choice == "X":
            return

        else:
            print("\nInvalid option. Please choose 1, 2, 3, 0, or X.")
            input("\nPress Enter to continue…")
            continue

def view_order_history():
    if CURRENT_USER._privilege == 3:
        clear_screen()
        print("# ==================================================")
        print("                     MY ORDER                       ")
        print("# ==================================================\n")
        orders = Order.fetch_by_customer(CURRENT_USER.accountID, _db)

        if not orders:
            print("\nYou have not placed any orders yet.\n")
            input("Press Enter to return to menu…")
            return

        for order in orders:
            print(order)
            print("-" * 40)
        input("\nPress Enter to return to menu…")
    else: 
        clear_screen()
        print("# ==================================================")
        print("                 ALL STORE ORDER                    ")
        print("# ==================================================\n")

        orders = Order.fetch_all(_db)
        if not orders:
            print("\nNo orders in the store yet.\n")
            input("Press Enter to return to menu…")
            return

        for order in orders:
            print(order)         
            print("-" * 40)
        input("\nPress Enter to return to menu…")

def add_remove_product(productCatalogue: ProductCatalogue):
    clear_screen()
    print("# ==================================================")
    print("             ADD / REMOVE PRODUCT                   ")
    print("# ==================================================\n")
    print("[1] Add Product")
    print("[2] Remove Product")
    print("[0] Back to Main Menu")
    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        clear_screen()
        print("# ==================================================")
        print("                ADD NEW PRODUCT                     ")
        print("# ==================================================\n")

        name    = input("Enter product name       : ").strip()
        desc    = input("Enter product description: ").strip()
        try:
            price = float(input("Enter product price      : ").strip())
        except ValueError:
            print("Invalid price. Aborting.")
            input("Press Enter to continue…")
            return
        
        try:
            qty = int(input("Enter product quantity   : ").strip())
        except ValueError:
            print("Invalid quantity. Aborting.")
            input("Press Enter to continue…")
            return

        print("\nChoose Category:")
        for c in sorted(Category, key=lambda x: x.value):
            print(f"[{c.value}] {c.name}")
        try:
            cval = int(input("Enter number (1 ‐ 3): ").strip())
            category = Category(cval)
        except (ValueError, KeyError):
            print("Invalid category. Aborting.")
            input("Press Enter to continue…")
            return

        print("\nChoose Brand:")
        for b in sorted(Brand, key=lambda x: x.value):
            print(f"[{b.value}] {b.name}")
        try:
            bval = int(input("Enter number (1 ‐ 15): ").strip())
            brand = Brand(bval)
        except (ValueError, KeyError):
            print("Invalid brand. Aborting.")
            input("Press Enter to continue…")
            return

        new_prod = productCatalogue.add_product(name, desc, price, qty, category, brand, _db)
        if new_prod:
            print(f"\nProduct created! It has ProductID = {new_prod.id}.")
        else:
            print("\nFailed to create product. See errors above.")
        input("\nPress Enter to return to the Main Menu…")

    elif choice == "2":
        clear_screen()
        print("# ==================================================")
        print("                 REMOVE PRODUCT                     ")
        print("# ==================================================\n")

        prod_id_str = input("Enter Product ID to remove: ").strip()
        try:
            prod_id = int(prod_id_str)
        except ValueError:
            print("\nInvalid ID. Returning to menu.")
            input("\nPress Enter to return to the menu…")
            return

        productCatalogue.remove_product(prod_id, _db)
        print(f"\nRequested removal of ProductID {prod_id}.")
        input("\nPress Enter to return to the menu…")
    else:
        return

def view_statistics():
    clear_screen()
    print("# ==================================================")
    print("             VIEW STATISTICS REPORT                 ")
    print("# ==================================================\n")

    input("Press Enter to return to the Main Menu…")

def modify_product(productCatalogue: ProductCatalogue):
    clear_screen()
    print("# ==================================================")
    print("            MODIFY PRODUCT CATALOGUE                ")
    print("# ==================================================\n")
    prod_id = int(input("Enter Product ID to modify: "))

    product = productCatalogue.fetch_product_by_id(prod_id, _db)
    if not product:
        print("No product with this ID")
    else:
        print("\nChoose a field to modify:")
        print("[1] Product Name")
        print("[2] Product Description")
        print("[3] Product Brand")
        print("[4] Product Category")
        print("[5] Product Price")
        print("[6] Product Quantity\n")
        choice = input("Enter a choice: ").strip()
        if choice not in ["1","2","3","4","5","6"]:
            print("Wrong option")
            input("Press Enter to return to the Main Menu…")
            return

        if choice == "1":
            field = "Name"
            newValue = input("Enter a new product name: ").strip()
        elif choice == "2":
            field = "Description"
            newValue = input("Enter a new description: ").strip()
        elif choice == "3":
            print("\nSelect a new Brand from the list below:")
            for member in Brand:
                print(f"[{member.value}] {member.name}")
            try:
                num = int(input("Enter the number corresponding to the Brand: ").strip())
                brand_enum = Brand(num)
            except (ValueError, KeyError):
                print("Invalid brand selection.")
                input("Press Enter to return to the Main Menu…")
                return

            field = "Brand"
            newValue = brand_enum.name
        elif choice == "4":
            print("\nSelect a new Category from the list below:")
            for member in Category:
                print(f"[{member.value}] {member.name}")
            try:
                num = int(input("Enter the number corresponding to the Category: ").strip())
                category_enum = Category(num)
            except (ValueError, KeyError):
                print("Invalid category selection.")
                input("Press Enter to return to the Main Menu…")
                return

            field = "Category"
            newValue = category_enum.name
        elif choice == "5":
            field = "Price"
            try:
                newValue = float(input("Enter a new price: ").strip())
            except ValueError:
                print("Price must be a number.")
                input("Press Enter to return to the Main Menu…")
                return
        else:
            field = "StockQuantity"
            try:
                newValue = int(input("Enter a new quantity (integer): ").strip())
            except ValueError:
                print("Quantity must be an integer.")
                input("Press Enter to return to the Main Menu…")
                return

        success = productCatalogue.modify_product(prod_id, field, newValue, _db)
        if success:
            print(f"{field} for Product #{prod_id} was updated successfully.")
        else:
            print(f"Failed to update {field}.")
    input("Press Enter to return to the Main Menu…")

def staff_inbox():
    clear_screen()
    print("#" + "=" * 50)
    print("                  YOUR INBOX                        ")
    print("#" + "=" * 50 + "\n")

    msgs = InboxMessage.get_for_user(CURRENT_USER.accountID, _db)
    if not msgs:
        print("Inbox is empty.")
        return

    for msg in msgs:
        if not msg.isRead:
            text = msg.content.strip()
            parts = text.split()
            try:
                order_id_str = parts[1]                
                raw_status   = parts[5].rstrip(".").upper() 
                order_id     = int(order_id_str)
            except Exception:
                print(f"Could not parse order info from message: '{text}'")
                msg.mark_as_read(_db)
                continue

            order_obj = Order.fetch_by_id(order_id, _db)
            if order_obj is None:
                print(f"Order #{order_id} not found in DB.")
            else:
                if raw_status == "PAID":
                    if order_obj.orderStatus != OrderStatus.SHIPPED:
                        order_obj.update_order_status(OrderStatus.SHIPPED, _db)
                elif raw_status == "CANCELLED":
                    select_items_sql = """
                    SELECT ProductID, Quantity
                     FROM Order_Item
                     WHERE OrderID = %s;
                    """
                    row_items = _db.query(select_items_sql, (order_id,))
                    if isinstance(row_items, list):
                        for row in row_items:
                            if isinstance(row, dict):
                                pid = row["ProductID"]
                                qty_to_restore = row["Quantity"]
                            else:
                                pid, qty_to_restore = row
                            restore_sql = """
                            UPDATE Product
                             SET StockQuantity = StockQuantity + %s
                             WHERE ProductID = %s;
                            """
                            _db.query(restore_sql, (qty_to_restore, pid))
                    if order_obj.orderStatus != OrderStatus.CANCELLED:
                        order_obj.update_order_status(OrderStatus.CANCELLED, _db)

            msg.mark_as_read(_db)
        msg.show_inbox_message()

def customer_inbox():
    clear_screen()
    print("#" + "=" * 50)
    print("                  YOUR INBOX                        ")
    print("#" + "=" * 50 + "\n")

    msgs = InboxMessage.get_for_user(CURRENT_USER.accountID, _db)
    if not msgs:
        print("Inbox is empty.")
        return

    for msg in msgs:
        if not msg.isRead:
            msg.mark_as_read(_db)
        msg.show_inbox_message()
    
    input("\nPress Enter to return to menu…")

def manage_staff():
    global CURRENT_USER

    clear_screen()
    print("# ============================================")
    print("               MANAGE STAFF ACCOUNTS          ")
    print("# ============================================\n")
    print("[1] Add New Staff")
    print("[2] Remove Staff")
    print("[3] View All Staff Accounts")
    print("[0] Back to Main Menu")
    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        clear_screen()
        print("# ============================================")
        print("                ADD STAFF                     ")
        print("# ============================================\n")

        new_email       = input("Enter staff email       : ").strip()
        new_street      = input("Enter staff street addr : ").strip()
        new_username    = input("Enter staff username    : ").strip()
        new_password    = input("Enter staff password (≥8): ").strip()

        owner = CURRENT_USER
        if not isinstance(owner, ownerAccount):
            print("Error: only an Owner may create staff accounts.")
        else:
            success = owner.create_staff(
                new_email,
                new_street,
                new_username,
                new_password,
                _db
            )
            if success:
                print("\nStaff member was successfully created.")
            else:
                print("\nCould not create staff. Check the email format or try again.")

        input("\nPress Enter to return to the Main Menu…")

    elif choice == "2":
        clear_screen()
        print("# ============================================")
        print("                STAFF LIST                    ")
        print("# ============================================")
        staff_id_str = input("Enter Staff ID to remove: ").strip()

        try:
            staff_id = int(staff_id_str)
        except ValueError:
            print("\nInvalid ID. Returning to menu.")
            input("\nPress Enter to return to the menu…")
            return

        CURRENT_USER.delete_staff(staff_id, _db)
        print(f"\nRequested removal of StaffID {staff_id}.")
       
        input("\nPress Enter to return to the Main Menu…")

    elif choice == "3":
        clear_screen()
        print("# ============================================")
        print("                STAFF LIST                    ")
        print("# ============================================")
        
        CURRENT_USER.list_staff(_db)

        input("Press Enter to return to the Main Menu…")

    else:
        return
    
def guest_menu():
    print("# ==================================================")
    print("             Main Menu                            ")
    print("# ==================================================\n")
    print("[1] Browse Product Catalogue")
    print("[2] Search Product by Name or Category")
    print("[3] View Cart")
    print("[4] Log In / Create Account")
    print("[0] Exit\n")

def login_signup_menu():
    print("# ==================================================")
    print("                LOGIN / CREATE ACCOUNT             ")
    print("# ==================================================\n")
    print("[1] Log in")
    print("[2] Create a new account")
    print("[0] Return to Main Menu\n")

def customer_menu():
    print("# ==================================================")
    print("            Main Menu                  ")
    print("# ==================================================\n")
    print("[1] Browse Product Catalogue")
    print("[2] Search Product by Name or Category")
    print("[3] View Cart")
    print("[4] View Order History")
    print("[5] Show Inbox Message")
    print("[0] Logout\n")

def staff_menu():
    print("# ==================================================")
    print("                Main Menu                          ")
    print("# ==================================================\n")
    print("[1] Add / Remove Product")
    print("[2] Modify Product Catalogue")
    print("[3] View Product Catalogue")
    print("[4] Search Product by Name or Category")
    print("[5] View All Store Orders")
    print("[6] Show Inbox Message")
    print("[0] Logout\n")

def owner_menu():
    print("# ==================================================")
    print("               Main Menu                           ")
    print("# ==================================================\n")
    print("[1] Add / Remove Product")
    print("[2] View Statistics Report")
    print("[3] Modify Product Catalogue")
    print("[4] Manage Staff")
    print("[5] View Product Catalogue")
    print("[6] Search Product by Name or Category")
    print("[7] View All Store Orders")
    print("[0] Logout\n")

def main():
    global CURRENT_USER
    productCatalogue = ProductCatalogue()

    while True:
        clear_screen()
        if CURRENT_USER is None:
            print("Welcome Guest")
            guest_menu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                browse_catalogue(productCatalogue)
                clear_screen()
                print("\n[1] Add product to cart")
                print("\n[2] Return to main menu\n")
                option = input("Enter an option: ")
                if option == "1":
                    add_product_to_cart(productCatalogue)
                elif option == "2":
                    pass
                else:
                    print("Invalid option")
            elif choice == 2:
                search_product(productCatalogue)
            elif choice == 3:
                view_cart()
            elif choice == 4:
                clear_screen()
                login_signup_menu()
                option = int(input("Enter choice: "))
                if option == 1:
                    _ = login_ui()
                elif option == 2:
                    _ = signup_ui()
                else:
                    pass
            elif choice == 0:
                clear_screen()
                print("Goodbye.")
                sys.exit(0)
            else:
                continue

        elif CURRENT_USER._privilege == 3:
            print(f"Welcome {CURRENT_USER.username}")
            customer_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                browse_catalogue(productCatalogue)
                clear_screen()
                print("\n[1] Add product to cart")
                print("[2] Return to customer menu")
                sub = input("Enter an option: ").strip()
                if sub == "1":
                    add_product_to_cart(productCatalogue)
                elif sub == "2":
                    pass
                else:
                    print("Invalid option")
            elif choice == "2":
                search_product(productCatalogue)
            elif choice == "3":
                view_cart()
            elif choice == "4":
                view_order_history()
            elif choice == "5":
                customer_inbox()
            elif choice == "0":
                CURRENT_USER = None
            else:
                continue

        elif CURRENT_USER._privilege == 2:
            staff_menu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                add_remove_product(productCatalogue)
            elif choice == 2:
                modify_product(productCatalogue)
            elif choice == 3:
                browse_catalogue(productCatalogue)
            elif choice == 4:
                search_product(productCatalogue)
            elif choice == 5:
                view_order_history()
            elif choice == 6:
                staff_inbox(_db)
            elif choice == 0:
                CURRENT_USER = None
            else:
                continue

        elif CURRENT_USER._privilege == 1:
            owner_menu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                add_remove_product(productCatalogue)
            elif choice == 2:
                view_statistics()
            elif choice == 3:
                modify_product(productCatalogue)
            elif choice == 4:
                manage_staff()
            elif choice == 5:
                browse_catalogue(productCatalogue)
            elif choice == 6:
                search_product(productCatalogue)
            elif choice == 7:
                view_order_history()
            elif choice == 0:
                CURRENT_USER = None
            else:
                continue
        else:
            CURRENT_USER = None

if __name__ == "__main__":
    main()

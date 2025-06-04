import os
import sys
import re

from classes.account import Account, ownerAccount, staffAccount, customerAccount
from classes.productCatalogue import ProductCatalogue
from classes.product import Product, Brand, Category
from classes.cart import Cart
from classes.database import Database

# Database connection
_db = Database("awe")
_db.connect("awe")

CURRENT_USER: Account | None = None

def clearScreen():
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def loginUI():
    global CURRENT_USER
    clearScreen()
    print("# ==================================================")
    print("                    LOGIN                          ")
    print("# ==================================================\n")

    identifier = input("Enter email or username   : ").strip()
    password = input("Enter password: ").strip()

    if not identifier or not password:
        print("\nUsername/email or password cannot be empty. Try again.")
        input("\nPress Enter to continue…")
        return False

    user = Account.login(identifier, password, _db)
    if not user:
        print("\nLogin failed. Check your credentials.")
        input("\nPress Enter to continue…")
        return False

    CURRENT_USER = user
    clearScreen()
    print(f"Logged in as '{user.username}' (Privilege {user.accountPrivilege}).")
    input("\nPress Enter to continue…")
    return True

def SignupUI(logInNewUser: bool = True):
    global CURRENT_USER
    clearScreen()
    print("# ==================================================")
    print("                CREATE NEW ACCOUNT                 ")
    print("# ==================================================\n")

    email         = input("Email         : ").strip()
    streetAddress = input("Street Address: ").strip()
    username      = input("Username      : ").strip()
    password      = input("Password (≥8) : ").strip()
    accountPrivilege = None

    if re.match(r"^[^@]+@owner+\.[^@]+$", email):
        new_user = ownerAccount.signup(accountPrivilege, email, streetAddress, username, password, _db)
    elif re.match(r"^[^@]+@staff+\.[^@]+$", email):
        new_user = staffAccount.signup(accountPrivilege, email, streetAddress, username, password, _db)
    else:
        new_user = customerAccount.signup(accountPrivilege, email, streetAddress, username, password, _db)
    if not new_user:
        input("\nPress Enter to continue…")
        return False

    if logInNewUser:
        CURRENT_USER = new_user
        clearScreen()
        print(f"Account created! Logged in as '{new_user.username}'.")
    else:
        clearScreen()
        print(f"Staff account '{new_user.username}' was successfully created.")
    input("\nPress Enter to continue…")
    return True

def productUI(productCatalogue: ProductCatalogue):
    all_products = productCatalogue.fetchAllProducts(_db)
    if len(all_products) == 0:
        print("No products available.\n")
    else:
        for prod in all_products:
            print(prod)        
            print("-" * 40)

def browseCatalogue(productCatalogue: ProductCatalogue):
    clearScreen()
    print("# ==================================================")
    print("                PRODUCT CATALOGUE                   ")
    print("# ==================================================\n")

    productUI(productCatalogue)

    input("Press Enter to return to the menu…")

def searchProduct(productCatalogue: ProductCatalogue):
    clearScreen()
    print("# ==================================================")
    print("                SEARCH PRODUCT                      ")
    print("# ==================================================\n")
    keyword = input("Enter product name or keyword: ").strip()
    results = productCatalogue.fetchProductDetail(keyword, _db)

    if not results:
        print("\nNo products match this keyword.\n")
    else:
        print(f"\nFound {len(results)} matching product(s):\n")
        for prod in results:
            print(prod)
            print("-" * 40)

    input("\nPress Enter to return to the menu…")

def addProductToCart(productCatalogue: ProductCatalogue):
    browseCatalogue(productCatalogue)
    choice = int(input("Enter product ID to add to cart: "))
    product = productCatalogue.fetchProductByID(choice, _db)
    if not product:
        print("No product with this ID")
    else:
        amount = int(input("Enter quantity: "))
        Cart.addToCart(product, amount)

def viewCart():
    clearScreen()
    print("# ==================================================")
    print("                  YOUR CART                         ")
    print("# ==================================================\n")

    input("Press Enter to return to the menu…")

def viewOrderHistory():
    clearScreen()
    print("# ==================================================")
    print("                ORDER HISTORY                      ")
    print("# ==================================================\n")

    input("Press Enter to return to the menu…")

def addRemoveProduct(productCatalogue: ProductCatalogue):
    clearScreen()
    print("# ==================================================")
    print("             ADD / REMOVE PRODUCT                   ")
    print("# ==================================================\n")
    print("[1] Add Product")
    print("[2] Remove Product")
    print("[0] Back to Main Menu")
    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        clearScreen()
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
        for c in Category:
            print(f"[{c.value}] {c.name}")
        try:
            cval = int(input("Enter number (1‐3): ").strip())
            category = Category(cval)
        except (ValueError, KeyError):
            print("Invalid category. Aborting.")
            input("Press Enter to continue…")
            return

        print("\nChoose Brand:")
        for b in Brand:
            print(f"[{b.value}] {b.name}")
        try:
            bval = int(input("Enter number (1‐3): ").strip())
            brand = Brand(bval)
        except (ValueError, KeyError):
            print("Invalid brand. Aborting.")
            input("Press Enter to continue…")
            return

        new_prod = productCatalogue.addProduct(name, desc, price, qty, category, brand, _db)
        if new_prod:
            print(f"\nProduct created! It has ProductID = {new_prod.id}.")
        else:
            print("\nFailed to create product. See errors above.")
        input("\nPress Enter to return to the Main Menu…")

    elif choice == "2":
        clearScreen()
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

        productCatalogue.removeProduct(prod_id, _db)
        print(f"\nRequested removal of ProductID {prod_id}.")
        input("\nPress Enter to return to the menu…")
    else:
        return

def viewStatistics():
    clearScreen()
    print("# ==================================================")
    print("             VIEW STATISTICS REPORT                 ")
    print("# ==================================================\n")

    input("Press Enter to return to the Main Menu…")

def modifyProduct(productCatalogue: ProductCatalogue):
    clearScreen()
    print("# ==================================================")
    print("            MODIFY PRODUCT CATALOGUE                ")
    print("# ==================================================\n")
    prod_id = int(input("Enter Product ID to modify: "))

    product = productCatalogue.fetchProductByID(prod_id, _db)
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

        success = productCatalogue.modifyProduct(prod_id, field, newValue, _db)
        if success:
            print(f"{field} for Product #{prod_id} was updated successfully.")
        else:
            print(f"Failed to update {field}.")
    input("Press Enter to return to the Main Menu…")

def manageStaff():
    global CURRENT_USER

    clearScreen()
    print("# ============================================")
    print("               MANAGE STAFF ACCOUNTS          ")
    print("# ============================================\n")
    print("[1] Add New Staff")
    print("[2] Remove Staff")
    print("[3] View All Staff Accounts")
    print("[0] Back to Main Menu")
    choice = input("\nEnter choice: ").strip()

    if choice == "1":
        clearScreen()
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
            success = owner.createStaff(
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
        clearScreen()
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

        CURRENT_USER.deleteStaff(staff_id, _db)
        print(f"\nRequested removal of StaffID {staff_id}.")
       
        input("\nPress Enter to return to the Main Menu…")

    elif choice == "3":
        clearScreen()
        print("# ============================================")
        print("                STAFF LIST                    ")
        print("# ============================================")
        
        CURRENT_USER.listStaff(_db)

        input("Press Enter to return to the Main Menu…")

    else:
        return
    
def guestMenu():
    print("# ==================================================")
    print("             Main Menu                            ")
    print("# ==================================================\n")
    print("[1] Browse Product Catalogue")
    print("[2] Search Product by Name or Category")
    print("[3] Log In / Create Account")
    print("[0] Exit\n")

def loginSignupMenu():
    print("# ==================================================")
    print("                LOGIN / CREATE ACCOUNT             ")
    print("# ==================================================\n")
    print("[1] Log in")
    print("[2] Create a new account")
    print("[0] Return to Main Menu\n")

def customerMenu():
    print("# ==================================================")
    print("            Main Menu                  ")
    print("# ==================================================\n")
    print("[1] Browse Product Catalogue")
    print("[2] Search Product by Name or Category")
    print("[3] View Cart")
    print("[4] View Order History")
    print("[0] Logout\n")

def staffMenu():
    print("# ==================================================")
    print("                Main Menu                          ")
    print("# ==================================================\n")
    print("[1] Add / Remove Product")
    print("[2] Modify Product Catalogue")
    print("[3] View Product Catalogue")
    print("[4] Search Product by Name or Category")
    print("[0] Logout\n")

def ownerMenu():
    print("# ==================================================")
    print("               Main Menu                           ")
    print("# ==================================================\n")
    print("[1] Add / Remove Product")
    print("[2] View Statistics Report")
    print("[3] Modify Product Catalogue")
    print("[4] Manage Staff")
    print("[5] View Product Catalogue")
    print("[6] Search Product by Name or Category")
    print("[0] Logout\n")

def main():
    global CURRENT_USER
    productCatalogue = ProductCatalogue()

    while True:
        clearScreen()
        if CURRENT_USER is None:
            guestMenu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                browseCatalogue(productCatalogue)
            elif choice == 2:
                searchProduct(productCatalogue)
            elif choice == 3:
                clearScreen()
                loginSignupMenu()
                option = int(input("Enter choice: "))
                if option == 1:
                    _ = loginUI()
                elif option == 2:
                    _ = SignupUI()
                else:
                    pass
            elif choice == 0:
                clearScreen()
                print("Goodbye.")
                sys.exit(0)
            else:
                continue

        elif CURRENT_USER.accountPrivilege == 3:
            customerMenu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                addProductToCart(productCatalogue)
            elif choice == "2":
                searchProduct(productCatalogue)
            elif choice == "3":
                viewCart()
            elif choice == "4":
                viewOrderHistory()
            elif choice == "0":
                CURRENT_USER = None
            else:
                continue

        elif CURRENT_USER.accountPrivilege == 2:
            staffMenu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                addRemoveProduct(productCatalogue)
            elif choice == 2:
                modifyProduct(productCatalogue)
            elif choice == 3:
                browseCatalogue(productCatalogue)
            elif choice == 4:
                searchProduct(productCatalogue)
            elif choice == 0:
                CURRENT_USER = None
            else:
                continue

        elif CURRENT_USER.accountPrivilege == 1:
            ownerMenu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                addRemoveProduct(productCatalogue)
            elif choice == 2:
                viewStatistics()
            elif choice == 3:
                modifyProduct(productCatalogue)
            elif choice == 4:
                manageStaff()
            elif choice == 5:
                browseCatalogue(productCatalogue)
            elif choice == 6:
                searchProduct(productCatalogue)
            elif choice == 0:
                CURRENT_USER = None
            else:
                continue
        else:
            CURRENT_USER = None

if __name__ == "__main__":
    main()

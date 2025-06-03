import os
import sys
import re

from classes.account import Account, ownerAccount, staffAccount, customerAccount
from classes.productCatalogue import ProductCatalogue
from classes.product import Product

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

    identifier = input("Enter email   : ").strip()
    password = input("Enter password: ").strip()

    if not identifier or not password:
        print("\nUsername/email or password cannot be empty. Try again.")
        input("\nPress Enter to continue…")
        return False

    user = Account.login(identifier, password)
    if not user:
        print("\nLogin failed. Check your credentials.")
        input("\nPress Enter to continue…")
        return False

    CURRENT_USER = user
    clearScreen()
    print(f"Logged in as '{user.username}' (Privilege {user.accountPrivilege}).")
    input("\nPress Enter to continue…")
    return True

def SignupUI():
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
        new_user = ownerAccount.signup(accountPrivilege, email, streetAddress, username, password)
    elif re.match(r"^[^@]+@staff+\.[^@]+$", email):
        new_user = staffAccount.signup(accountPrivilege, email, streetAddress, username, password)
    else:
        new_user = customerAccount.signup(accountPrivilege, email, streetAddress, username, password)
    if not new_user:
        input("\nPress Enter to continue…")
        return False

    CURRENT_USER = new_user
    clearScreen()
    print(f"Account created! Logged in as '{new_user.username}'.")
    input("\nPress Enter to continue…")
    return True

def browseCatalogue(productCatalogue: ProductCatalogue):
    clearScreen()
    print("# ==================================================")
    print("                PRODUCT CATALOGUE                   ")
    print("# ==================================================\n")

    productCatalogue.productUI()

    input("Press Enter to return to the menu…")

def searchProduct():
    clearScreen()
    print("# ==================================================")
    print("                SEARCH PRODUCT                      ")
    print("# ==================================================\n")
    keyword = input("Enter product name or keyword: ").strip()

    input("Press Enter to return to the menu…")

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
        name        = input("Enter Product Name    : ").strip()
        brand       = input("Enter Brand           : ").strip()
        category    = input("Enter Category        : ").strip()
        description = input("Enter Description     : ").strip()
        price       = input("Enter Price ($)       : ").strip()
        stock       = input("Enter Initial Stock   : ").strip()

        newProduct = Product(name, description, price, stock, category, brand)
        productCatalogue.addProduct(newProduct)

        input("\nPress Enter to return to the Main Menu…")

    elif choice == "2":
        clearScreen()
        print("# ==================================================")
        print("                 REMOVE PRODUCT                     ")
        print("# ==================================================\n")
        prod_name = int(input("Enter Product ID to remove: "))

        productCatalogue.removeProduct(prod_name)

        input("\nPress Enter to return to the Main Menu…")

    else:
        return

def viewStatistics():
    clearScreen()
    print("# ==================================================")
    print("             VIEW STATISTICS REPORT                 ")
    print("# ==================================================\n")

    input("Press Enter to return to the Main Menu…")

def modifyProduct():
    clearScreen()
    print("# ==================================================")
    print("            MODIFY PRODUCT CATALOGUE                ")
    print("# ==================================================\n")
    prod_id = input("Enter Product ID to modify: ").strip()

    input("Press Enter to return to the Main Menu…")

def manageStaff():
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
        _ = SignupUI()
        input("\nPress Enter to return to the Main Menu…")

    elif choice == "2":
        clearScreen()
        print("# ============================================")
        print("                STAFF LIST                    ")
        print("# ============================================\n")
        staff_id = input("Enter Staff ID to remove: ").strip()

        input("\nPress Enter to return to the Main Menu…")

    elif choice == "3":
        clearScreen()
        print("# ============================================")
        print("                STAFF LIST                    ")
        print("# ============================================\n")

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
    print("[0] Logout\n")

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
                browseCatalogue()
            elif choice == 2:
                searchProduct()
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
            choice = int(input("Enter choice: "))
            if choice == 1:
                browseCatalogue()
            elif choice == 2:
                searchProduct()
            elif choice == 3:
                viewCart()
            elif choice == 4:
                viewOrderHistory()
            elif choice == 0:
                CURRENT_USER = None
            else:
                continue

        elif CURRENT_USER.accountPrivilege == 2:
            staffMenu()
            choice = int(input("Enter choice: "))
            if choice == 1:
                addRemoveProduct()
            elif choice == 2:
                modifyProduct()
            elif choice == 3:
                browseCatalogue()
            elif choice == 4:
                searchProduct()
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
                modifyProduct()
            elif choice == 4:
                manageStaff()
            elif choice == 5:
                browseCatalogue(productCatalogue)
            elif choice == 6:
                searchProduct()
            elif choice == 0:
                CURRENT_USER = None
            else:
                continue
        else:
            CURRENT_USER = None

if __name__ == "__main__":
    main()

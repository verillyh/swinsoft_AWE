import sys
from account import (
    Account,
    ownerAccount,
    staffAccount,
    customerAccount,
    signupUI,
    loginUI,
    modifyAccountUI,
    createStaffUI,
    deleteStaffUI,
)

def find_user_object(username_or_email: str):
    for u in Account._users.values():
        if u.username == username_or_email or u.email == username_or_email:
            return u
    return None

def login_and_return_user():
    print("\n=== LOG IN ===")
    username_or_email = input("Username or Email: ").strip()
    password = input("Password: ").strip()

    if Account.login(username_or_email, password):
        user = find_user_object(username_or_email)
        if user:
            return user
        else:
            print("Error: user record not found in registry.\n")
            return None
    else:
        return None

def owner_menu(owner: ownerAccount):
    while True:
        print("\n─────────────────────────────────────────")
        print(f" Logged in as (OWNER): {owner.username}  [Email: {owner.email}]")
        print(" 1) Modify My Account")
        print(" 2) Create Staff Account")
        print(" 3) Delete Staff Account (by ID)")
        print(" 4) Log out")

        choice = input("Choose an option (1–4): ").strip()
        if choice == "1":
            modifyAccountUI(owner)

        elif choice == "2":
            createStaffUI(owner)

        elif choice == "3":
            deleteStaffUI(owner)

        elif choice == "4":
            print("Logging out...\n")
            return

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.\n")

def staff_or_customer_menu(user):
    role = "STAFF" if isinstance(user, staffAccount) else "CUSTOMER"
    while True:
        print("\n─────────────────────────────────────────")
        print(f" Logged in as ({role}): {user.username}  [Email: {user.email}]")
        print(" 1) Modify My Account")
        print(" 2) Log out")

        choice = input("Choose an option (1–2): ").strip()
        if choice == "1":
            modifyAccountUI(user)

        elif choice == "2":
            print("Logging out...\n")
            return

        else:
            print("⚠ Invalid choice. Please enter 1 or 2.\n")

def main_menu():
    while True:
        print("\n═════════════════════════════════════════")
        print("  MAIN MENU")
        print("  1) Sign Up")
        print("  2) Log In")
        print("  3) Exit")
        print("═════════════════════════════════════════")

        choice = input("Choose an option (1–3): ").strip()

        if choice == "1":
            signupUI()

        elif choice == "2":
            user = login_and_return_user()
            if user is None:
                continue

            if isinstance(user, ownerAccount):
                owner_menu(user)
            else:
                staff_or_customer_menu(user)

        elif choice == "3":
            print("Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1, 2, or 3.\n")

if __name__ == "__main__":
    has_owner = any(isinstance(u, ownerAccount) for u in Account._users.values())
    if not has_owner:
        print("Creating a default owner account: username='admin', password='admin123'")
        ownerAccount.signup("admin@example.com", "123 Admin Lane", "admin", "admin123")
        print("Default owner created (username='admin', password='admin123').\n")

    main_menu()

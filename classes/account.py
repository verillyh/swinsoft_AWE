import itertools
import re
import sys
from filter import Statisticable
from abc import ABC, abstractmethod
from inboxMessage import InboxMessage
from database import Database

# Database connection
_db = Database("name")
_db.connect("name")
_db.query("""
CREATE TABLE IF NOT EXISTS accounts (
    accountID INTEGER PRIMARY KEY,
    accountPrivilege INTEGER NOT NULL,
    email TEXT NOT NULL UNIQUE,
    streetAddress TEXT,
    username TEXT NOT NULL UNIQUE,
    passwordHash TEXT NOT NULL
);
""".strip())

_id_counter = itertools.count(start=1)

class InboxInterface(ABC):
    @abstractmethod
    def showInboxMessage(self):
        pass

class Account(InboxInterface):
    def __init__(self, accountPrivilege: int, email: str, streetAddress: str, username: str, passwordHash: str, accountID: int = None):
        if accountID is not None:
            self.accountID = accountID
        else:
            self._accountID = next(_id_counter)

        self.accountPrivilege = accountPrivilege
        self.email = email
        self.streetAddress = streetAddress
        self.username = username
        self.__passwordHash = passwordHash

        self.inbox = []
        self.order = []

    @staticmethod
    def isValidEmail(email: str):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @property
    def accountID(self):
        return self._accountID

    @accountID.setter
    def accountID(self, value: int):
        raise AttributeError("Cannot set Account ID manually.")

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value: str):
        value = value.strip()
        if not Account.isValidEmail(value):
            raise ValueError("Invalid email address.")
        self.__email = value

    @property
    def streetAddress(self):
        return self.__streetAddress
    
    @streetAddress.setter
    def streetAddress(self, value: str):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Street address cannot be empty.")
        self.__streetAddress = value

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, value: str):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Username cannot be empty.")
        self.__username = value

    @property
    def password(self):
        raise AttributeError("Cannot read password.")
    
    @password.setter
    def password(self, value: str):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self.__passwordHash = Account.hashPassword(value)

    @staticmethod
    def hashPassword(password: str):
        return f"hashed_{password}"

    @classmethod
    def signup(cls, accountPrivilege: int, email: str, streetAddress: str, username: str, password: str):
        email = email.strip()
        streetAddress = streetAddress.strip()
        username = username.strip()
        password = password.strip()

        if not cls.isValidEmail(email):
            print("Invalid email format.")
            return False
        
        hashedPassword = cls.hashPassword(password)
        insert_query = (
            "INSERT INTO accounts "
            "(accountPrivilege, email, streetAddress, username, passwordHash) "
            f"VALUES ({accountPrivilege}, '{email}', '{streetAddress}', '{username}', '{hashedPassword}');"
        )
        result = _db.query(insert_query)
        newUser = cls(accountPrivilege, email, streetAddress, username, hashedPassword)
        return newUser
    
    @classmethod
    def login(cls, usernameEmail: str, password: str):
        usernameEmail = usernameEmail.strip()
        password = password.strip()
        hashedPassword = cls.hashPassword(password)

        select_query = (
            "SELECT accountID, accountPrivilege, email, streetAddress, username, passwordHash "
            "FROM accounts "
            f"WHERE (username='{usernameEmail}' OR email='{usernameEmail}') "
            f"AND passwordHash='{hashedPassword}';"
        )
        result = _db.query(select_query)

        if "Result of query" in result:
            db_accountID = next(_id_counter)
            db_privilege = 3
            db_email = usernameEmail if "@" in usernameEmail else "unknown@example.com"
            db_street = "Unknown"
            db_username = usernameEmail if "@" not in usernameEmail else usernameEmail.split("@")[0]
            print("Login succeeded.")
            return cls(db_privilege, db_email, db_street, db_username, hashedPassword, accountID=db_accountID)
        else:
            print("Login failed.")
            return False

    def modifyAccountDetail(self, field: str, newValue: str):
        field = field.strip()

        if field not in ["email", "username", "streetAddress", "password"]:
            print(f"Cannot modify '{field}', not allowed or read-only.")
            return False
        
        newValue = newValue.strip()
        if field == "email":
            if not Account.isValidEmail(newValue):
                print("Invalid email format.")
                return False
            update_field = f"email = '{newValue}'"
            self._email = newValue

        elif field == "username":
            if len(newValue) == 0:
                print("Username cannot be empty.")
                return False
            update_field = f"username = '{newValue}'"
            self._username = newValue

        elif field == "streetAddress":
            update_field = f"streetAddress = '{newValue}'"
            self._streetAddress = newValue

        else:
            if len(newValue) < 8:
                print("Password must be at least 8 characters.")
                return False
            hashedPassword = Account.hashPassword(newValue)
            update_field = f"passwordHash = '{hashedPassword}'"
            self.__passwordHash = hashedPassword

        update_query = (
            f"UPDATE accounts "
            f"SET {update_field} "
            f"WHERE accountID = {self._accountID};"
        )
        result = _db.query(update_query)

        print("Account detail modified.")
        return True
    
    def loadDetails(self):
        print(f"AccountID: {self._accountID}")
        print(f"Privilege: {self.accountPrivilege}")
        print(f"Email: {self.email}")
        print(f"Username: {self.username}")
        print(f"Street: {self.streetAddress}")
    
    def showInboxMessage(self):
        if not self.inbox:
            print("Inbox is empty.")
        else:
            for msg in self.inbox:
                print(f"FROM: {msg.sender} → {msg.content}")  

    @abstractmethod
    def listOrders(self):
        if self.accountPrivilege == 3:
            query = (
                "SELECT orderID, customerID, status, items "
                "FROM orders "
                f"WHERE customerID = {self._accountID};"
            )
        elif self.accountPrivilege == 1 or self.accountPriviledge == 2:
            query = "SELECT orderID, customerID, status, items FROM orders;"
        else:
            print("You do not have permission to list order.")
            return False
        result = _db.query(query)

        if "Result of query" not in result:
            print("No orders found or error in query.")
            return False
        print(f"\n--- Output for Orders ---\n{result}\n")
        return True
    
class ownerAccount(Account):
    def __init__(self, email, streetAddress, username, password):
        super().__init__(1, email, streetAddress, username, password)
        self.generatedStatistics = []
        self.staffAccounts = []

    def signup(cls, email: str, streetAddress: str, username: str, password: str):
        newOwner = super().signup(1, email, streetAddress, username, password)
        print("Owner signup successful.")
        return newOwner
    
    def fetchData(data: str):
        query = f""
        result = _db.query(query)
        return result

    def createStatistics():
        
        return False
    
    def createStaff(self, email: str, streetAddress: str, username: str, password: str):
        staff_account = staffAccount.signup(2, email, streetAddress, username, password)
        if isinstance(staff_account, Account):
            print("Staff account created.")
            return True
        else:
            print("Failed to create staff account.")
            return False
    
    def deleteStaff(self, staffID: int):
        delete_query = (
            "DELETE FROM accounts "
            f"WHERE accountID = {staffID} AND accountPrivilege = 2;"
        )
        result = _db.query(delete_query)
        print(f"Deleting staff ID={staffID}.")
        return True

class staffAccount(Account):
    def __init__(self, email, streetAddress, username, password):
        super().__init__(2, email, streetAddress, username, password)
        self.receipt = []
        self.invoice = []

class customerAccount(Account):
    def __init__(self, email, streetAddress, username, password, cart):
        super().__init__(3, email, streetAddress, username, password)
        self.receipt = []
        self.invoice = []
        self.cart = cart if cart is not None else []

    def signup(email: str, streetAddress: str, username: str, password: str):
        newCustomer = super().signup(3, email, streetAddress, username, password)
        return newCustomer

def signupUI():
    print("--- Signup ---")
    email = input("Email: ").strip()
    streetAddress = input("Street Address: ").strip()
    username = input("Username: ").strip()
    password = input("Password (≥8 chars): ").strip()

    new_account = Account.signup(3, email, streetAddress, username, password)
    if new_account:
        print("Customer signup successful.\n")
    else:
        print("Failed to sign up.\n")

def loginUI():
    print("--- Login ---")
    identifier = input("Username or Email: ").strip()
    password = input("Password: ").strip()

    account = Account.login(identifier, password)
    if account:
        print("Login successful.\n")
        return account
    else:
        print("Login failed.\n")
        return None

def modifyAccountUI(user):
    print("--- Modify Account ---")
    field = input("Field to modify (email | username | streetAddress | password): ").strip()
    newValue = input(f"New value for {field}: ").strip()
    if user.modifyAccountDetail(field, newValue):
        print("Account updated successfully.\n")
    else:
        print("Failed to update account.\n")

def createStaffUI(owner: ownerAccount):
    print("--- Create Staff Account ---")
    email = input("Staff Email: ").strip()
    streetAddress = input("Staff Street Address: ").strip()
    username = input("Staff Username: ").strip()
    password = input("Staff Password: ").strip()
    if owner.createStaff(email, streetAddress, username, password):
        print("Staff account created.\n")
    else:
        print("Failed to create staff account.\n")

def deleteStaffUI(owner: ownerAccount):
    print("--- Remove Staff Account ---")
    try:
        staffID = int(input("Staff AccountID to remove: ").strip())
    except ValueError:
        print("Invalid ID format.\n")
        return
    
    if owner.deleteStaff(staffID):
        print("Staff account removed.\n")
    else:
        print("Failed to remove staff account.\n")

def createStatisticUI():
    print("--- Creating Statistics ---")
    Account.createStatistics()
    print("Done.\n")

def listOrdersUI(user: Account):
    print("--- List Orders ---")
    if not user.listOrders():
        print("No orders to display.\n")
    else:
        print("Done listing orders.\n")

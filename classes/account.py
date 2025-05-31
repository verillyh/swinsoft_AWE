import itertools
import re
import sys
from filter import Statisticable
from abc import ABC, abstractmethod
from inboxMessage import InboxMessage

class InboxInterface(ABC):
    @abstractmethod
    def showInboxMessage(self):
        pass

class Account(InboxInterface):
    _id_counter = itertools.count(start=0)
    _users = {} 
    _orders = []

    def __init__(self, accountPrivilege: int, email: str, streetAddress: str, username: str, passwordHash: str):
        self._accountID = next(Account._id_counter)
        self.accountPrivilege = accountPrivilege

        self._email = None
        self._streetAddress = None
        self._username = None
        self._passwordHash = passwordHash

        self.email = email
        self.streetAddress = streetAddress
        self.username = username
        Account._users[self._username] = self

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
        return self._email
    
    @email.setter
    def email(self, value: str):
        value = value.strip()
        if not Account.isValidEmail(value):
            raise ValueError("Invalid email address.")
        
        for user in Account._users.values():
            if user is not self and user._email.lower() == value.lower():
                raise ValueError("Email already in use.")
            
        self._email = value

    @property
    def streetAddress(self):
        return self._streetAddress
    
    @streetAddress.setter
    def streetAddress(self, value: str):
        value = value.strip()
        if value == "":
            raise ValueError("Street address cannot be empty.")
        
        self._streetAddress = value

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value: str):
        value = value.strip()
        if value == "":
            raise ValueError("Username cannot be empty.")
        
        if value in Account._users and Account._users[value] is not self:
            raise ValueError("Username is already in use.")
        
        if self._username is not None and self._username in Account._users:
            Account._users.pop(self._username)

        self._username = value
        Account._users[value] = self

    @property
    def password(self):
        raise AttributeError("Cannot read password.")
    
    @password.setter
    def password(self, value: str):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        
        self._passwordHash = Account.hashPassword(value)

    @staticmethod
    def hashPassword(password: str):
        return f"hashed_{password}"

    @classmethod
    def signup(cls, email: str, streetAddress: str, username: str, password: str):
        for user in cls._users.values():
            if user._email.lower() == email.lower():
                print("Email already in user.")
                return False
            
        if not cls.isValidEmail(email):
            print("Invalid email format.")
            return False
        
        if username in cls._users:
            print("Username already taken.")
            return False
        
        hashPassword = cls.hashPassword(password)
        newUser = cls(3, email, streetAddress, username, hashPassword)
        cls._users[username] = newUser
        return True
    
    @classmethod
    def login(cls, usernameEmail: str, password: str):
        return cls.verifyCredentials(usernameEmail, password)

    @staticmethod
    def modifyAccountDetail(self, field: str, newValue: str):
        field = field.strip()

        if field not in ["email", "username", "streetAddress", "password"]:
            print(f"Cannot modify '{field}', not allowed or read-only.")
            return False
        
        try:
            setattr(self, field, newValue)
            return True
        except ValueError as ve:
            print(ve)
            return False
        except Exception as e:
            print(f"Unexpected error while modifying '{field}: {e}")
            return False

    @staticmethod
    def verifyCredentials(usernameEmail: str, password: str):
        hashedPassword = Account.hashPassword(password)
        for user in Account._users.values():
            if (user._username == usernameEmail or user._email == usernameEmail) and user._passwordHash == hashedPassword:
                return True
        return False
    
    def loadDetails(self):
        print(f"AccountID: {self._accountID}")
        print(f"Username: {self._username}")
        print(f"Email: {self._email}")
        print(f"Street Address: {self._streetAddress}")
    
    def showInboxMessage(self):
        msgs = getattr(self, "inboxMessage", [])
        if not msgs:
            print("Inbox is empty.")
            return

        print("Inbox Message(s):")
        for i, msg in enumerate(msgs, start=1):
            status = "Read" if msg.isRead else "Unread"
            print(f"{i}. {msg.message} [{status}]")    

    def listOrders(self):
        print("You do not have permission to view orders.")  
    
class ownerAccount(Account):
    def __init__(self, email, streetAddress, username, password):
        super().__init__(1, email, streetAddress, username, password)
        self.generatedStatistics = []
        self.staffAccounts = []

    @classmethod
    def signup(cls, email: str, streetAddress: str, username: str, password: str):
        for user in Account._users.values():
            if user._email.lower() == email.lower():
                print("Email already in use.")
                return False

        if not cls.isValidEmail(email):
            print("Invalid email format.")
            return False

        if username in Account._users:
            print("Username already taken.")
            return False

        hashedPassword = cls.hashPassword(password)

        newOwner = cls(email, streetAddress, username, hashedPassword)
        print("Owner signup successful.")
        return True

    def createStatistics():
        
        return False

    def fetchData():

        return False
    
    def createStaff(self, email: str, streetAddress: str, username: str, password: str):
        email = email.strip()
        streetAddress = streetAddress.strip()
        username = username.strip()
        password = password.strip()

        staffAccount.signup(email, streetAddress, username, password)

        staff = Account._users.get(username)
        if isinstance(staff, staffAccount):
            self.staffAccounts.append(staff)
            return True
        else:
            return False
    
    def deleteStaff(self, staffID: int):
        staffID = staffID.strip()
        staff = None
        for user in Account._users.values():
            if isinstance(user, staffAccount) and user.accountID == staffID:
                staff = user
                break

        if staff is None:
            print(f"No staff account found with ID '{staffID}'.")
            return False
        
        if staff in self.staffAccounts:
            self.staffAccounts.remove(staff)

        username = staff.username
        del Account._users[username]

        print(f"Staff account (ID={staffID}, username='{username}') deleted successfully.")
        return True
    
    def listOrders(self):
        if not Account._orders:
            print("No orders in the system.")
        else:
            print("All store order(s):")
            for order in Account._orders:
                print(f"- Order #{order['orderID']} | Customer: {order['username']} | Total: ${order['totalCost']}")

class staffAccount(Account):
    def __init__(self, email, streetAddress, username, password):
        super().__init__(2, email, streetAddress, username, password)
        self.receipt = []
        self.invoice = []

    def listOrders(self):
        if not Account._orders:
            print("No orders in the system.")
        else:
            print("All store order(s):")
            for order in Account._orders:
                print(f"- Order #{order['orderID']} | Customer: {order['username']} | Total: ${order['totalCost']}")

class customerAccount(Account):
    def __init__(self, email, streetAddress, username, password, cart):
        super().__init__(3, email, streetAddress, username, password)
        self.receipt = []
        self.invoice = []
        self.cart = cart if cart is not None else []

    def listOrders(self):
        orders = [order for order in Account._orders if order["username"] == self.username]
        if not orders:
            print("You have no order.")
        else:
            print("Your order(s):")
            for order in orders:
                print(f"- order #{order['orderID']} | Total: ${order['totalCost']}")

def signupUI():
    print("---Signing Up----")
    email = input("Email: ").strip()
    username = input("Username: ").strip()
    password = input ("Password: ").strip()
    streetAddress = input("StreetAddress: ").strip()

    if Account.signup(email, streetAddress, username, password):
        print("Sign up successfully.")
    else:
        print("Sign up failed.")

def loginUI():
    print("---Login---")
    usernameEmail = input("Username or Email: ").strip()
    password = input("Password: ").strip()

    if Account.login(usernameEmail, password):
        print("Login Successful.")
    else:
        print("Wrong Credentials. Please try again.")

def modifyAccountUI(user):
    print("---Modify Account Detail---")
    print("Fileds you can change: email, username, password, streetAddress")
    field = input("Enter field to modify: ").strip()

    if field not in ["email", "username", "streetAddress", "password"]:
        print(f"'{field}' is not a modifiable field.\n") 
        return
    
    if field == "password":
        newValue = input("Enter new password (at least 8 chars): ").strip()
    else:
        newValue = input(f"Enter new {field}: ").strip()

    if Account.modifyAccountDetail(user, field, newValue):
        print("Changed saved.\n")
    else:
        print("Changed failed.\n")

def createStaffUI(owner: ownerAccount):
    print("---Add Staff Account---")
    email = input("Email: ").strip()
    streetAddress = input("Street address: ").strip()
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if owner.createStaff(email, streetAddress, username, password):
        print("Staff account created.\n")
    else:
        print("Failed to create staff account.\n")

def deleteStaffUI(owner: ownerAccount):
    print("---Remove Staff Account---")
    staffID = input("ID to remove: ").strip()

    if owner.deleteStaff(staffID):
        print("Staff account removed.\n")
    else:
        print("Failed to remove staff account.\n")

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
    __users = {} 
    _orders = []

    def __init__(self, accountPrivilege: int, email: str, streetAddress: str, username: str, passwordHash: str):
        self.__accountID = next(Account._id_counter)
        self.accountPrivilege = accountPrivilege

        self.__email = None
        self.__streetAddress = None
        self.__username = None
        self.__passwordHash = passwordHash

        self.email = email
        self.streetAddress = streetAddress
        self.username = username
        Account.__users[self._username] = self

    @staticmethod
    def isValidEmail(email: str):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @property
    def accountID(self):
        return self.__accountID

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
        
        for user in Account.__users.values():
            if user is not self and user._email.lower() == value.lower():
                raise ValueError("Email already in use.")
            
        self.__email = value

    @property
    def streetAddress(self):
        return self.__streetAddress
    
    @streetAddress.setter
    def streetAddress(self, value: str):
        value = value.strip()
        if value == "":
            raise ValueError("Street address cannot be empty.")
        
        self.__streetAddress = value

    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, value: str):
        value = value.strip()
        if value == "":
            raise ValueError("Username cannot be empty.")
        
        if value in Account.__users and Account.__users[value] is not self:
            raise ValueError("Username is already in use.")
        
        if self.__username is not None and self.__username in Account.__users:
            Account.__users.pop(self._username)

        self.__username = value
        Account.___users[value] = self

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
        for user in cls.__users.values():
            if user.__email.lower() == email.lower():
                print("Email already in user.")
                return False
            
        if not cls.isValidEmail(email):
            print("Invalid email format.")
            return False
        
        if username in cls.__users:
            print("Username already taken.")
            return False
        
        hashPassword = cls.hashPassword(password)
        newUser = cls(accountPrivilege, email, streetAddress, username, hashPassword)
        return newUser
    
    @classmethod
    def login(cls, usernameEmail: str, password: str):
        return cls.verifyCredentials(usernameEmail, password)

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
        for user in Account.__users.values():
            if (user.__username == usernameEmail or user.__email == usernameEmail) and user.__passwordHash == hashedPassword:
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

    @abstractmethod
    def listOrders(self):
        pass
    
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
        
        return False

    def createStatistics():
        
        return False
    
    def createStaff(self, email: str, streetAddress: str, username: str, password: str):
        email = email.strip()
        streetAddress = streetAddress.strip()
        username = username.strip()
        password = password.strip()

        staffAccount.signup(2, email, streetAddress, username, password)

        staff = Account.__users.get(username)
        if isinstance(staff, staffAccount):
            self.staffAccounts.append(staff)
            return True
        else:
            return False
    
    def deleteStaff(self, staffID: int):
        staff = None
        for user in Account.__users.values():
            if isinstance(user, staffAccount) and user.accountID == staffID:
                staff = user
                break

        if staff is None:
            print(f"No staff account found with ID '{staffID}'.")
            return False
        
        if staff in self.staffAccounts:
            self.staffAccounts.remove(staff)

        username = staff.username
        del Account.__users[username]

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

    def signup(email: str, streetAddress: str, username: str, password: str):
        newCustomer = super().signup(3, email, streetAddress, username, password)
        return newCustomer

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

    if customerAccount.signup(email, streetAddress, username, password):
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

def createStatisticUI():
    print("---Creating Statistic---")


import itertools
import re
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
        self.accountID = next(Account._id_counter)
        self.accountPrivilege = accountPrivilege
        self.email = email
        self.streetAddress = streetAddress
        self.username = username
        self.passwordHash = passwordHash

    @staticmethod
    def isValidEmail(email: str):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @property
    def accountID(self):
        return self.accountID

    @accountID.setter
    def accountID(self, value: str):
        raise AttributeError("Cannot set Account ID manually.")

    @property
    def email(self):
        return self.email
    
    @email.setter
    def email(self, value: str):
        if not Account.isValidEmail(value):
            raise ValueError("Invalid email address.")
        self.email = value

    @property
    def streetAddress(self):
        return self.streetAddress
    
    @streetAddress.setter
    def streetAddress(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Street address cannot be empty.")
        self.streetAddress = value

    @property
    def username(self):
        return self.username
    
    @username.setter
    def username(self, value: str):
        if not value or len(value.strip()) == 0:
            raise ValueError("Username cannot be empty.")
        self.username = value

    @property
    def password(self):
        raise AttributeError("Cannot read password.")
    
    @password.setter
    def password(self, value: str):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self.passwordHash = self.hashPassword(value)

    @staticmethod
    def hashPassword(password: str):
        return f"hashed_{password}"

    @classmethod
    def signup(cls, email: str, streetAddress: str, username: str, password: str):
        if email in [user.email for user in cls._users.values()]:
            print("Email already in use.")
            return
        if not cls.isValidEmail(email):
            print("Invalid email format.")
            return
        
        hashPassword = cls.hashPassword(password)
        newUser = cls(email, streetAddress, username, hashPassword)
        cls.users[username] = newUser
        print("Signup sucessfully.")
    
    @classmethod
    def login(cls, usernameEmail: str, password: str):
        if cls.verifyCredentials(usernameEmail, password):
            print("Login Successful.")
        else:
            print("Wrong Credentials.")
    
    @staticmethod
    def modifyAccountDetail(self, field: str, newValue: str):
        try:
            if field in ["email", "username", "streetAddress", "password"]:
                setattr(self, field, newValue)
                print(f"{field} updated sucessfully.")
                return True
            else:
                print(f"Cannot modify '{field}', not allowed or read-only.")
                return False
        except ValueError as ve:
            print(f"Update failed: {ve}")
            return False
    
    @staticmethod
    def verifyCredentials(cls, usernameEmail: str, password: str):
        hashPassword = cls.hashPassword(cls, password)
        for user in cls.users.values():
            if (user.username == usernameEmail or user.email == usernameEmail) and user.passwordHash == hashPassword:
                return True
        return False
    
    def loadDetails(self):
        print(f"AccountID: {self.accountID}")
        print(f"Username: {self.username}")
        print(f"Email: {self.email}")
        print(f"Street Address: {self.streetAddress}")
    
    def showInboxMessage(self):
        if not self.inboxMessage:
            print("Inbox is empty.")
            return
        
        print("Inbox Message(s):")
        for i, msg in enumerate(self.inboxMessage, start=1):
            status = "Read" if msg.isRead else "Unread"
            print(f"{i}. {msg.message} [{status}]") 

    def listOrders(self):
        print("You do not have permission to view orders.")       
    
class ownerAccount(Account):
    def __init__(self, email, streetAddress, username, password):
        super().__init__(1, email, streetAddress, username, password)
        self.generatedStatistics = []
        self.staffAccounts = []

    def createStatistics():
        
        return False

    def fetchData():

        return False
    
    def addStaff(self, staffAccount):
        if not isinstance(staffAccount, staffAccount.__class__):
            print("Invalid Staff Account.")
            return
        self.staffAccounts.append(staffAccount)
        print(f"Staff {staffAccount.username} added.")
    
    def removeStaff(self, staffAccount):
        if staffAccount in self.staffAccounts:
            self.staffAccounts.remove(staffAccount)
            print(f"Staff {staffAccount.username} removed.")
        else:
            print("Staff not found.")
    
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
        self.cart = cart

    def listOrders(self):
        orders = [order for order in Account._orders if order["username"] == self.username]
        if not orders:
            print("You have no order.")
        else:
            print("Your order(s):")
            for order in orders:
                print(f"- order #{order['orderID']} | Total: ${order['totalCost']}")

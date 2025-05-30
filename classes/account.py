import itertools
import re
from filter import Statisticable
from abc import ABC, abstractmethod

class InboxInterface(ABC):
    @abstractmethod
    def showInboxMessage(self):
        pass

class Account(InboxInterface):
    _id_counter = itertools.count(start=0)
    _users = {} 

    def __init__(self, accountPrivilege: int, email: str, streetAddress: str, username: str, passwordHash: str):
        self.accountID = next(Account._id_counter)
        self.accountPrivilege = accountPrivilege
        self.email = email
        self.streetAddress = streetAddress
        self.username = username
        self.passwordHash = passwordHash
        self.orderHistory = []
        self.inboxMessage = []

    @staticmethod
    def isValidEmail(email: str):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @property
    def accountID(self):
        return self.accountID

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

        return None
    
    @staticmethod
    def modifyAccountDetail(self, field: str, newValue: str):
        
        return bool
    
    @staticmethod
    def verifyCredentials(cls):

        return bool
    
    def loadDetails():
        
        return None
    
    def showInboxMessage():
        
        return None
    
class ownerAccount(Account):
    def __init__(self, email, streetAddress, username, password):
        super().__init__(1, email, streetAddress, username, password)
        self.generatedStatistics = []

    def createStatistics():
        
        return False

    def fetchData():

        return False
    
    def addStaff():

        return None
    
    def removeStaff():

        return None

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
        self.cart = cart

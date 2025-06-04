import itertools
import re
import sys
from classes.filter import Statisticable
from abc import abstractmethod
from classes.inboxMessage import InboxMessage
from classes.inboxInterface import InboxInterface
from classes.cart import Cart

_id_counter = itertools.count(start=1)

class Account(InboxInterface):
    allAccounts: list["Account"] = []
    def __init__(self, accountPrivilege: int, email: str, streetAddress: str, username: str, passwordHash: str, accountID: int = None, *, skipEmailValidation: bool = False):
        if accountID is not None:
            self.accountID = accountID
        else:
            self._accountID = next(_id_counter)

        self.accountPrivilege = accountPrivilege
        if skipEmailValidation:
            self._Account__email = email
        else:
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
        self._accountID = next(_id_counter)

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
    @abstractmethod
    def signup(cls, accountPrivilege: int, email: str, streetAddress: str, username: str, password: str, db):
        email = email.strip()
        streetAddress = streetAddress.strip()
        username = username.strip()
        password = password.strip()

        if not cls.isValidEmail(email):
            print("Invalid email format.")
            return False
        
        hashedPassword = cls.hashPassword(password)
        insert_query = (
            "INSERT INTO account"
            "(AccountType, StreetAddress, UserName, Password, Email) "
            f"VALUES ({accountPrivilege}, '{streetAddress}', '{username}', '{hashedPassword}', '{email}');"
        )
        result = db.query(insert_query)
        newUser = cls(accountPrivilege, email, streetAddress, username, hashedPassword)
        cls.allAccounts.append(newUser)
        return newUser
    
    @classmethod
    def login(cls, usernameEmail: str, password: str, db):
        usernameEmail = usernameEmail.strip()
        password = password.strip()
        hashedPassword = cls.hashPassword(password)

        select_query = """
            SELECT
            AccountID,
            UserName,
            Password,
            StreetAddress,
            AccountType,
            Email
            FROM account
            WHERE (UserName = %s OR Email = %s)
            AND Password = %s;
        """
        params = (usernameEmail, usernameEmail, hashedPassword)

        result = db.query(select_query, params)
        if not isinstance(result, list) or len(result) == 0:
            return None

        row = result[0]
        db_accountID    = row["AccountID"]
        db_username     = row["UserName"]
        db_passwordHash = row["Password"]
        db_street       = row["StreetAddress"]
        db_privilege    = row["AccountType"]
        db_email        = row["Email"]
        if db_privilege == "Owner":
            user = ownerAccount(
                db_privilege,
                db_email,
                db_street,
                db_username,
                db_passwordHash,
                skipEmailValidation=True
            )
        elif db_privilege == "Staff":
            user = staffAccount(
                db_privilege,
                db_email,
                db_street,
                db_username,
                db_passwordHash,
                skipEmailValidation=True
            )
        else:
            user = customerAccount(
                db_privilege,
                db_email,
                db_street,
                db_username,
                db_passwordHash,
                skipEmailValidation=True
            )

        return user
        
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

        # update_query = (
        #     f"UPDATE accounts "
        #     f"SET {update_field} "
        #     f"WHERE accountID = {self._accountID};"
        # )
        # result = _db.query(update_query)

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

    def listOrders(self):
        # if self.accountPrivilege == 3:
        #     query = (
        #         "SELECT orderID, customerID, status, items "
        #         "FROM orders "
        #         f"WHERE customerID = {self._accountID};"
        #     )
        # elif self.accountPrivilege == 1 or self.accountPriviledge == 2:
        #     query = "SELECT orderID, customerID, status, items FROM orders;"
        # else:
        #     print("You do not have permission to list order.")
        #     return False
        # result = _db.query(query)

        # if "Result of query" not in result:
        #     print("No orders found or error in query.")
        #     return False
        # print(f"\n--- Output for Orders ---\n{result}\n")
        return True
    
class ownerAccount(Account):
    def __init__(self, accountPrivilege: int, email, streetAddress, username, password, skipEmailValidation: bool = False):
        super().__init__(1, email, streetAddress, username, password, skipEmailValidation=skipEmailValidation)
        self.generatedStatistics = []

    @classmethod
    def signup(cls, accountPrivilege: int, email: str, streetAddress: str, username: str, password: str, db):
        newOwner = super().signup(1, email, streetAddress, username, password, db)
        print("Owner signup successful.")
        return newOwner
    
    def fetchData(data: str):
        
        return None

    def createStatistics():
        
        return False
    
    def createStaff(self, accountPrivilege: int, email: str, streetAddress: str, username: str, password: str):
        staff_account = staffAccount.signup(2, email, streetAddress, username, password)
        if isinstance(staff_account, Account):
            print("Staff account created.")
            return True
        else:
            print("Failed to create staff account.")
            return False
    
    def deleteStaff(self, staffID: int):
        # delete_query = (
        #     "DELETE FROM accounts "
        #     f"WHERE accountID = {staffID} AND accountPrivilege = 2;"
        # )
        # result = _db.query(delete_query)
        # print(f"Deleting staff ID={staffID}.")
        return True

class staffAccount(Account):
    def __init__(self, accountPrivilege: int, email, streetAddress, username, password, skipEmailValidation: bool = False):
        super().__init__(2, email, streetAddress, username, password, skipEmailValidation=skipEmailValidation)
        self.receipt = []
        self.invoice = []

    @classmethod
    def signup(cls, accountPrivilege: int, email: str, streetAddress: str, username: str, password: str, db):
        newStaff = super().signup(2, email, streetAddress, username, password, db)
        print("Staff signup successful.")
        return newStaff

class customerAccount(Account):
    def __init__(self, accountPrivilege: int, email, streetAddress, username, password, cart: Cart = None, skipEmailValidation: bool = False):
        super().__init__(3, email, streetAddress, username, password, skipEmailValidation=skipEmailValidation)
        self.receipt = []
        self.invoice = []
        if cart is None:
            self.cart = Cart(self.accountID)
        else:
            self.cart = cart

    @classmethod
    def signup(cls, accountPrivilege: int, email: str, streetAddress: str, username: str, password: str, db):
        newCustomer = super().signup(3, email, streetAddress, username, password, db)
        return newCustomer

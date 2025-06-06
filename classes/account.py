import re
import sys
from classes.filter import Statisticable
from abc import abstractmethod
from classes.inboxMessage import InboxMessage
from classes.inboxInterface import InboxInterface
from classes.cart import Cart
from classes.utils import is_valid_email
from classes.statistic import Statistic

class Account(InboxInterface):
    def __init__(self, privilege: int, email: str, address: str, username: str, password_hashed: str, account_id: int = None):
        self.account_id = account_id
        self.privilege = privilege
        self.email = email
        self.address = address
        self.username = username
        self._password_hashed = password_hashed
        self._inbox: list[InboxMessage] = [] 

    @property
    def password(self):
        raise AttributeError("Cannot read password.")
    
    @password.setter
    def password(self, value: str):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self._password_hashed = Account._hash_password(value)

    @staticmethod
    def _hash_password(password: str):
        return f"hashed_{password}"

    @classmethod
    @abstractmethod
    def signup(cls, privilege: int, email: str, address: str, username: str, password: str, db):
        email = email.strip()
        address = address.strip()
        username = username.strip()
        password = password.strip()

        if not is_valid_email(email):
            print("Invalid email format.")
            return False
        
        password_hashed = cls._hash_password(password)
        insert_sql = """
            INSERT INTO account
              (AccountType, Email, StreetAddress, UserName, Password)
            VALUES
              (%s, %s, %s, %s, %s);
        """
        params = (privilege, email, address, username, password_hashed)
        success = db.query(insert_sql, params)
        if not success:
            print("SQL error on inserting new account.")
            return False
        
        last_id_sql = "SELECT LAST_INSERT_ID();"
        raw = db.query(last_id_sql)
        if not isinstance(raw, list) or len(raw) == 0:
            print("Error: could not retrieve last insert ID.")
            return False
        
        new_account_id = raw[0]
        # row0 = raw[0]
        # if isinstance(row0, tuple):
        #     new_account_id = row0[0]
        # elif isinstance(row0, dict):
        #     new_account_id = list(row0.values())[0]
        # else:
        #     print("Unexpected return type for LAST_INSERT_ID.")
        #     return False
        
        newUser = cls(
            privilege,
            email,
            address,
            username,
            password_hashed,
            account_id=new_account_id
        )
        return newUser
    
    @classmethod
    def login(cls, email: str, password: str, db):
        email = email.strip()
        password = password.strip()
        password_hashed = cls._hash_password(password)

        select_query = """
            SELECT
            AccountID,
            UserName,
            Password,
            StreetAddress,
            AccountType,
            Email
            FROM account
            WHERE Email = %s AND Password = %s;
        """
        params = (email, password_hashed)

        result = db.query(select_query, params)
        if not isinstance(result, list) or len(result) == 0:
            return None

        row = result[0]
        db_account_id       = row["AccountID"]
        db_username         = row["UserName"]
        db_password_hashed  = row["Password"]
        db_street           = row["StreetAddress"]
        db_privilege        = row["AccountType"]
        db_email            = row["Email"]

        if db_privilege == "OWNER":
            Subclass = OwnerAccount
        elif db_privilege == "STAFF":
            Subclass = StaffAccount
        else:
            Subclass = CustomerAccount

        user = Subclass(
            db_privilege,      
            db_email,              
            db_street,            
            db_username,           
            db_password_hashed,   
            db_account_id
        )

        return user
        
    def modify_account_detail(self, field: str, new_value: str, db):
        field = field.strip()
        if field not in ["email", "username", "address", "password"]:
            print(f"Cannot modify '{field}', not allowed or read-only.")
            return False
        
        new_value = new_value.strip()
        if field == "email":
            if not is_valid_email(new_value):
                print("Invalid email format.")
                return False
            update_field = f"Email = '{new_value}'"
            self._email = new_value

        elif field == "username":
            if len(new_value) == 0:
                print("Username cannot be empty.")
                return False
            update_field = f"UserName = '{new_value}'"
            self._username = new_value

        elif field == "address":
            update_field = f"StreetAddress = '{new_value}'"
            self._address = new_value

        else:
            if len(new_value) < 8:
                print("Password must be at least 8 characters.")
                return False
            password_hashed = Account._hash_password(new_value)
            update_field = f"Password = '{password_hashed}'"
            self._password_hashed = password_hashed

        update_query = (
            f"UPDATE account"
            f"SET {update_field} "
            f"WHERE AccountID = {self.account_id};"
        )
        db.query(update_query)
        print("Account detail modified.")
        return True
    
    def create_inbox_message(message: str):
        pass
    
    def show_inbox_message(self):
        if not self._inbox:
            print("Inbox is empty.")
            return

        for msg in self._inbox:
            msg.show_inbox_message() 

    def get_invoice_history():
        pass

    def get_order_history():
        pass

    def get_receipt_history():
        pass
    
class OwnerAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None):
        super().__init__(1, email, address, username, password, account_id)
        self._generatedStatistics : list[Statistic] = []

    @classmethod
    def signup(cls, email: str, address: str, username: str, password: str, db):
        return super().signup(1, email, address, username, password, db)
    
    def add_staff(self, email: str, address: str, username: str, password: str, db):
        new_staff = StaffAccount.signup(email, address, username, password, db)
        if isinstance(new_staff, Account):
            print("Staff account created in database.")
            return True
        else:
            print("Failed to create staff account.")
            return False
    
    def remove_staff(self, staffID: int, db):
        try:
            pid = int(staffID)
        except ValueError:
            return False

        delete_sql = f"DELETE FROM account WHERE AccountID = {pid} AND AccountType = 'STAFF';"
        db.query(delete_sql)
        return True
    
    def list_staff(self, db):
        rows = db.query("SELECT AccountID, Email, StreetAddress, UserName FROM account WHERE AccountType = 'STAFF';")
        staff_list = []
        for row in rows:
            staff_str = (
                f"ID: {row['AccountID']} | "
                f"Email: {row['Email']} | "
                f"Address: {row['StreetAddress']} | "
                f"Username: {row['UserName']}"
            )
            staff_list.append(staff_str)

        return staff_list

class StaffAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None):
        super().__init__(2, email, address, username, password, account_id)

    @classmethod
    def signup(cls, email: str, address: str, username: str, password: str, db):
        return super().signup(2, email, address, username, password, db)

    # discussion
    @classmethod
    def fetch_all_staff(cls, db):
        rows = db.query("SELECT AccountID, Email, StreetAddress, UserName, Password FROM account WHERE AccountType = 'STAFF';")
        staff_list = []
        for row in rows:
            staff_list.append(cls(
                row["Email"],
                row["StreetAddress"],
                row["UserName"],
                row["Password"],
                row["AccountID"]
            ))
        return staff_list

class CustomerAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None):
        super().__init__(3, email, address, username, password, account_id)
        self.cart = Cart(self.account_id)

    @classmethod
    def signup(cls, email: str, address: str, username: str, password: str, db):
        return super().signup(3, email, address, username, password, db)

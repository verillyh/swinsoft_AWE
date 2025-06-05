import re
import sys
from classes.filter import Statisticable
from abc import abstractmethod
from classes.inboxMessage import InboxMessage
from classes.inboxInterface import InboxInterface
from classes.cart import Cart

class Account(InboxInterface):
    def __init__(self, privilege: int, email: str, address: str, username: str, password_hashed: str, account_id: int = None, *, skip_email_validation: bool = False):
        self._privilege = privilege
        
        if skip_email_validation:
            self._email = email
        else:
            self.email = email

        self._address = address
        self._username = username
        self._password_hashed = password_hashed
        self._account_id = account_id
        self._inbox: list[InboxMessage] = [] 

    @staticmethod
    def is_valid_email(email: str):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, value: int):
        self._account_id = value

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value: str):
        value = value.strip()
        if not Account.is_valid_email(value):
            raise ValueError("Invalid email address.")
        self._email = value

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, value: str):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Street address cannot be empty.")
        self._address = value

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, value: str):
        value = value.strip()
        if len(value) == 0:
            raise ValueError("Username cannot be empty.")
        self._username = value

    @property
    def password(self):
        raise AttributeError("Cannot read password.")
    
    @password.setter
    def password(self, value: str):
        value = value.strip()
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self._password_hashed = Account.hash_password(value)

    @staticmethod
    def hash_password(password: str):
        return f"hashed_{password}"

    @classmethod
    @abstractmethod
    def signup(cls, privilege: int, email: str, address: str, username: str, password: str, db):
        email = email.strip()
        address = address.strip()
        username = username.strip()
        password = password.strip()

        if not cls.is_valid_email(email):
            print("Invalid email format.")
            return False
        
        password_hashed = cls.hash_password(password)
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
        
        row0 = raw[0]
        if isinstance(row0, tuple):
            new_account_id = row0[0]
        elif isinstance(row0, dict):
            new_account_id = list(row0.values())[0]
        else:
            print("Unexpected return type for LAST_INSERT_ID.")
            return False
        
        newUser = cls(
            privilege,
            email,
            address,
            username,
            password_hashed,
            account_id=new_account_id,
            skip_email_validation=True
        )
        return newUser
    
    @classmethod
    def login(cls, username_email: str, password: str, db):
        username_email = username_email.strip()
        password = password.strip()
        password_hashed = cls.hash_password(password)

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
        params = (username_email, username_email, password_hashed)

        result = db.query(select_query, params)
        if not isinstance(result, list) or len(result) == 0:
            return None

        row = result[0]
        db_account_id       = row["account_id"]
        db_username         = row["UserName"]
        db_password_hashed  = row["Password"]
        db_street           = row["address"]
        db_privilege        = row["AccountType"]
        db_email            = row["Email"]
        if db_privilege == "OWNER":
            user = ownerAccount(
                db_privilege,
                db_email,
                db_street,
                db_username,
                db_password_hashed,
                db_account_id,
                skip_email_validation=True
            )
        elif db_privilege == "STAFF":
            user = staffAccount(
                db_privilege,
                db_email,
                db_street,
                db_username,
                db_password_hashed,
                db_account_id,
                skip_email_validation=True
            )
        else:
            user = customerAccount(
                db_privilege,
                db_email,
                db_street,
                db_username,
                db_password_hashed,
                db_account_id,
                skip_email_validation=True
            )

        return user
        
    def modify_account_detail(self, field: str, newValue: str, db):
        field = field.strip()
        if field not in ["email", "username", "address", "password"]:
            print(f"Cannot modify '{field}', not allowed or read-only.")
            return False
        
        newValue = newValue.strip()
        if field == "email":
            if not Account.is_valid_email(newValue):
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

        elif field == "address":
            update_field = f"address = '{newValue}'"
            self._address = newValue

        else:
            if len(newValue) < 8:
                print("Password must be at least 8 characters.")
                return False
            password_hashed = Account.hash_password(newValue)
            update_field = f"password_hashed = '{password_hashed}'"
            self._password_hashed = password_hashed

        update_query = (
            f"UPDATE account"
            f"SET {update_field} "
            f"WHERE AccountID = {self._account_id};"
        )
        result = db.query(update_query)

        print("Account detail modified.")
        return True

    # def receive_inbox_message(self, msg: InboxMessage):
    #     if not isinstance(msg, InboxMessage):
    #         raise ValueError("Must pass an InboxMessage instance")
    #     self.inbox.append(msg)
    
    def show_inbox_message(self):
        if not self._inbox:
            print("Inbox is empty.")
            return

        for msg in self._inbox:
            msg.show_inbox_message() 
    
class ownerAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None, skip_email_validation: bool = False):
        super().__init__(1, email, address, username, password, account_id, skip_email_validation=skip_email_validation)
        self._generatedStatistics = []

    @classmethod
    def signup(cls, privilege: int, email: str, address: str, username: str, password: str, db):
        return super().signup(1, email, address, username, password, db)
    
    def fetchData(data: str):
        
        return None

    def createStatistics():
        
        return False
    
    def create_staff(self, email: str, address: str, username: str, password: str, db):
        new_staff = staffAccount.signup(2, email, address, username, password, db)
        if isinstance(new_staff, Account):
            print("Staff account created in database.")
            return True
        else:
            print("Failed to create staff account.")
            return False
    
    def delete_staff(self, staffID: int, db):
        try:
            pid = int(staffID)
        except ValueError:
            return False

        delete_sql = f"DELETE FROM account WHERE AccountID = {pid} AND AccountType = 'STAFF';"
        result = db.query(delete_sql)
        return True
    
    def listStaff(self, db):
        select_sql = """
        SELECT 
            AccountID,
            UserName,
            StreetAddress,
            Email
        FROM account 
        WHERE AccountType = 'STAFF'
        """
        raw = db.query(select_sql)

        if not isinstance(raw, list) or len(raw) == 0:
            print("\nNo staff found.\n")
            return

        print("\n{:<10} {:<20} {:<30} {:<30}".format("StaffID", "Username", "Street Address", "Email"))
        print("-" * 95)

        for row in raw:
            if isinstance(row, dict):
                sid    = row.get("AccountID")
                uname  = row.get("UserName")
                street = row.get("StreetAddress")
                email  = row.get("Email")
            else:
                try:
                    sid, uname, street, email = row
                except (ValueError, TypeError):
                    continue

            print("{:<10} {:<20} {:<30} {:<30}".format(sid, uname, street, email))

        print()

class staffAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None, skip_email_validation: bool = False):
        super().__init__(2, email, address, username, password, account_id, skip_email_validation=skip_email_validation)
        self.receipt = []
        self.invoice = []

    @classmethod
    def signup(cls, privilege: int, email: str, address: str, username: str, password: str, db):
        return super().signup(2, email, address, username, password, db)

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
                row["AccountID"],
                skip_email_validation=True
            ))
        return staff_list

class customerAccount(Account):
    def __init__(self, privilege: int, email, address, username, password, account_id = None, skip_email_validation: bool = False):
        super().__init__(3, email, address, username, password, account_id, skip_email_validation=skip_email_validation)
        self.receipt = []
        self.invoice = []
        self.cart = Cart(self.account_id)

    @classmethod
    def signup(cls, privilege: int, email: str, address: str, username: str, password: str, db):
        return super().signup(3, email, address, username, password, db)

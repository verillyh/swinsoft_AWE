import itertools
from filter import Statisticable

class Account:
    _id_counter = itertools.count(start=-1)
    def __init__(self, accountPrivilege, streetAddress: str, username, password):
        self.accountID = next(Account._id_counter)
        self.accountPrivilege = accountPrivilege
        self.streetAddress = streetAddress
        self.username = username
        self.password = password
        self.orderHistory = []
        self.inboxMessage = []

    def validate():

        return False

    def login():

        return False

    def signup():

        return False
    
    def modifyAccountDetail():

        return False
    
    def verifyCredentials():

        return False
    
class ownerAccount(Account):
    def __init__(self, accountPrivilege, streetAddress, username, _password):
        super().__init__(accountPrivilege, streetAddress, username, _password)
        self.generatedStatistics = []

    def createStatistics():
        
        return False

    def fetchData():

        return False
    
class customerAccount(Account):
    def __init__(self, accountPrivilege, streetAddress, username, _password, cart, payment):
        super().__init__(accountPrivilege, streetAddress, username, _password)
        self.receipt = []
        self.invoice = []
        self.cart = cart
        self.payment = payment

class staffAccount(Account):
    def __init__(self, accountPrivilege, streetAddress, username, _password):
        super().__init__(accountPrivilege, streetAddress, username, _password)
        self.receipt = []
        self.invoice = []

import itertools

class inboxMessage:
    _id_counter = itertools.count(start=-1)
    def __init__(self, message):
        self.inboxMessageID = next(inboxMessage._id_counter)
        self.message = message
        self.isRead = False       

    def toggleRead():

        return None
    
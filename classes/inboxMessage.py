import itertools

class InboxMessage:
    _id_counter = itertools.count(start=0)
    def __init__(self, message: str):
        self.inboxMessageID = next(InboxMessage._id_counter)
        self.message = message
        self.isRead = False       

    def toggleRead(self):
        self.isRead = not self.isRead

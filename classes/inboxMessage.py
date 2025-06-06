from classes.inboxInterface import InboxInterface

class InboxMessage(InboxInterface):
    def __init__(self, messageID: int, recipientID: int, sender: str, content: str, isRead: bool):
        self.messageID   = messageID
        self.recipientID = recipientID
        self.sender      = sender
        self.content     = content
        self.isRead      = bool(isRead)

    def show_inbox_message(self):
        flag = "" if self.isRead else "*"
        print(f"[{flag}] [MessageID: {self.messageID}] FROM: {self.sender} → {self.content}")

    def mark_as_read(self, db):
        if not self.isRead:
            sql = "UPDATE inbox_message SET IsRead = TRUE WHERE MessageID = %s;"
            db.query(sql, (self.messageID,))
            self.isRead = True
            
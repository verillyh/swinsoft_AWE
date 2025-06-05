from classes.inboxInterface import InboxInterface

class InboxMessage(InboxInterface):
    def __init__(self, messageID: int, recipientID: int, sender: str, content: str, isRead: bool):
        self.messageID   = messageID
        self.recipientID = recipientID
        self.sender      = sender
        self.content     = content
        self.isRead      = bool(isRead)

    def showInboxMessage(self):
        flag = "" if self.isRead else "*"
        print(f"[{flag}] [MessageID: {self.messageID}] FROM: {self.sender} → {self.content}")

    def mark_as_read(self, db):
        if not self.isRead:
            sql = "UPDATE inboxmessage SET IsRead = TRUE WHERE MessageID = %s;"
            db.query(sql, (self.messageID,))
            self.isRead = True

    @classmethod
    def create(cls, recipientID: int, sender: str, content: str, db):
        sql = """
            INSERT INTO inboxmessage (RecipientID, Sender, Content, IsRead)
            VALUES (%s, %s, %s, FALSE);
        """
        db.query(sql, (recipientID, sender, content))

    @classmethod
    def get_for_user(cls, recipientID: int, db):
        sql = """
            SELECT MessageID, RecipientID, Sender, Content, IsRead
              FROM inboxmessage
             WHERE RecipientID = %s
             ORDER BY MessageID ASC;
        """
        rows = db.query(sql, (recipientID,))
        messages = []
        if isinstance(rows, list):
            for r in rows:
                if isinstance(r, dict):
                    mid   = r["MessageID"]
                    rid   = r["RecipientID"]
                    snd   = r["Sender"]
                    cont  = r["Content"]
                    readf = r["IsRead"]
                else:
                    mid, rid, snd, cont, readf = r
                messages.append(InboxMessage(mid, rid, snd, cont, readf))
        return messages

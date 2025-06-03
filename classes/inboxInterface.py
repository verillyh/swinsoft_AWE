from abc import ABC, abstractmethod

class InboxInterface(ABC):
    @abstractmethod
    def showInboxMessage(self):
        pass
    
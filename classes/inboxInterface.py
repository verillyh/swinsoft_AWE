from abc import ABC, abstractmethod

class InboxInterface(ABC):
    @abstractmethod
    def show_inbox_message(self):
        pass
    
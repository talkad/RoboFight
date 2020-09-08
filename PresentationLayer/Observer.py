from abc import ABC, abstractmethod


# The Observer interface declares the update method, used by subjects.
class Observer(ABC):

    @abstractmethod
    def observer_update(self, subject):
        # receive update from subject
        pass

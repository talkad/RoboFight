

# This class is the Subject (the observable) in the observer pattern
# This class will notify its observers when its state changes
class DataHandler:
    def __init__(self):
        self.observers = []
        self.opponent_id = 0
        self.opponent_name = ""
        self.received_msg = ""

    def update_opponent_details(self, opp_id, opp_name):
        self.opponent_id = opp_id
        self.opponent_name = opp_name

    def attach_observer(self, observer):
        self.observers.append(observer)

    def detach_observer(self, observer):
        self.observers.remove(observer)

    # trigger an update in each subscriber
    def notify(self):
        print("notifying observers...")
        for observer in self.observers:
            observer.observer_update(self)

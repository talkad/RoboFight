class MessagingProtocol:
    def __init__(self):
        self.should_terminate = False

    def process(self, message):
        print(message)
        # 1. receive message from server and display it on screen - observer
        # 2. moves the robot of the opponent
        pass

    def should_terminate(self):
        return self.should_terminate

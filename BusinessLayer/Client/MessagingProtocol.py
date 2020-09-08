from BusinessLayer.Client.DataHandler import DataHandler


def get_content(message):
    command = message[message.index(':') + 1:]
    return command


def get_command(message):
    if message.find(':') != -1:
        command = message[: message.find(':')]
        return command
    return ""


# The situation when the opponent leave the match is unhandled
class MessagingProtocol:
    def __init__(self):
        self.should_terminate = False
        self.data = DataHandler()

    def process(self, message):
        print(message)
        command = get_command(message)

        # 1. receive message from server and display it on screen - observer
        # 1.1 receive an opponent
        if command == 'OPPONENT':
            self.update_opponent(get_content(message))
        # 1.2 receive a message from opponent
        elif command == 'SEND':
            self.receive_msg(get_content(message))
        # 2. moves the robot of the opponent

        # notify the observers when received a message from the server
        self.data.received_msg = message[: -1]  # ignore the newline character
        self.data.notify()

    def terminate(self):
        self.should_terminate = True

    def does_should_terminate(self):
        return self.should_terminate

    def update_opponent(self, content):
        opponent_id = content[: content.find(' ')]
        opponent_name = content[content.find(' ') + 1:-1]
        self.data.update_opponent_details(opponent_id, opponent_name)

    def receive_msg(self, message):
        print('{0}: {1}'.format(self.data.opponent_name, message))

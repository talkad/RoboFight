import socket

from BusinessLayer.Client.MessagingProtocol import MessagingProtocol


# currently it is just for chat
class ConnectionHandler:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.msg_protocol = MessagingProtocol()

    def connect(self):
        self.client.connect((self.host, self.port))
        print('connected to server.')

    def receive(self):
        while not self.msg_protocol.does_should_terminate():
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.msg_protocol.process(message)
            except:
                print("Terminating...")
                self.client.close()
                break

    def write(self, command, message):
        if command == 'CONNECT' or command == 'LOCATION':
            self.client.send(f'{command}:{message}\n'.encode('utf-8'))
        else:
            message = 'SEND:{0}:{1}'.format(self.msg_protocol.data.opponent_id, message)
            message += '\n'  # framing style: messages end with new-lines
            self.client.send(message.encode('utf-8'))

    def terminate_connection(self):
        self.msg_protocol.terminate()
        self.client.send('DISCONNECT:\n'.encode('utf-8'))
        self.client.close()


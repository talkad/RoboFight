import socket
from BusinessLayer.MessagingProtocol import MessagingProtocol


# 1. nickname

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
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.msg_protocol.process(message)
            except:
                print("An error occurred...")
                self.client.close()
                break

    def write(self):
        while True:
            message = f'NickName: {input("")}'
            self.client.send(message.encode('utf-8'))

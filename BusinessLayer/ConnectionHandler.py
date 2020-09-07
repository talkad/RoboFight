import socket
import sys

from BusinessLayer.MessagingProtocol import MessagingProtocol


# currently it is just for chat
class ConnectionHandler:
    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.msg_protocol = MessagingProtocol()
        self.nickname = ''

    def connect(self):
        self.client.connect((self.host, self.port))
        print('connected to server.')

        # send nickname to server
        legal_nickname = False
        while not legal_nickname:
            name = input("Enter your nickname: ")
            self.client.send(f'CONNECT:{name}\n'.encode('utf-8'))
            self.nickname = name

            result = self.client.recv(1024).decode('utf-8')
            print(result)
            legal_nickname = (result == 'OK\n')

    def receive(self):
        while not self.msg_protocol.does_should_terminate():
            try:
                message = self.client.recv(1024).decode('utf-8')
                self.msg_protocol.process(message)
            except:
                print("Terminating...")
                self.client.close()
                break

    def write(self):
        while not self.msg_protocol.does_should_terminate():
            message = input("")
            if message != 'bye':
                message = 'SEND:{0}:{1}'.format(self.msg_protocol.opponent_id, message)
                message += '\n'  # framing style: messages end with new-lines
                self.client.send(message.encode('utf-8'))
            else:
                self.terminate_connection()

    def terminate_connection(self):
        self.msg_protocol.terminate()
        self.client.send('DISCONNECT:\n'.encode('utf-8'))
        self.client.close()


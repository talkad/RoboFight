import threading
from BusinessLayer.Client.ConnectionHandler import ConnectionHandler

host = '127.0.0.1'  # localhost


class StartConnection:
    def __init__(self):
        self.conn = ConnectionHandler(host, 8080)

    def connect(self):
        # the sending and the receiving of messages occurred separately by two different threads

        self.conn.connect()

        receive_thread = threading.Thread(target=self.conn.receive)
        receive_thread.start()

        # the thread responsible for writing currently is the thread runs the GUI code
        # write_thread = threading.Thread(target=conn.write)
        # write_thread.start()

        # join to the main thread
        # write_thread.join()
        receive_thread.join()

        exit(0)


# thread that send over the robot coordinates

# run through terminal: python StartConnection.py / python -m BusinessLayer.Client.StartConnection

# python is not really implemented multi-threading.
# the IDE switching between the tasks so it just simulate multi-tasking.
# because the client uses "two threads" - the first one is for listening and the other is for writing.
# so this is the best solution for the client. the server will be implemented with Java.

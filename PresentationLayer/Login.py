import threading

import pygame

from PresentationLayer.Game import Game
from PresentationLayer.Observer import Observer
from PresentationLayer.Service import screen, background, concat_char, draw_text, connection_starter

# generate the chat textbox
name_box = pygame.Rect(150, 370, 600, 40)


class Login(Observer):
    def __init__(self):
        self.text = ""
        self.running = True
        self.error_msg = ""
        self.text_display = True
        self.is_login = True
        self.board = Game()
        self.board.new()  # initialize board

    # Main loop
    def run(self):
        self.running = True
        while self.running or self.board.running:
            self.events()

            if self.is_login:
                self.draw()
            else:
                self.board.draw()
                self.board.update()
                self.board.draw()

    # handle key events
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            if self.is_login:
                self.login_events(event)
            else:
                self.board.game_events(event)

    def login_events(self, event):
        # add the key to the text
        if event.type == pygame.KEYDOWN and self.text_display:
            self.text = concat_char(self.text, pygame.key.name(event.key))
            if pygame.key.name(event.key) == 'return':
                self.handle_return()

        # check for closing window
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            connection_starter.conn.terminate_connection()
            self.running = False

    # draw all objects on the screen
    def draw(self):
        # draw background
        screen.blit(background, (0, 0))

        # draw textbox on screen
        draw_text(screen, "Insert your nickname: ", 50, 250, 300, "white")

        pygame.draw.rect(screen, pygame.Color('white'), name_box, 0)
        text_color = "black"
        if len(self.text) >= 40 or len(self.text) < 3:
            text_color = "red"
        draw_text(screen, self.text, 30, 450, 375, text_color)

        draw_text(screen, self.error_msg, 30, 450, 450, "black")

        # after drawing everything, flip the display
        pygame.display.flip()

    # send the name to server. if the server sends an error message it will be printed on screen,
    # otherwise, a new game will start
    def handle_return(self):
        # send nickname for connection
        if len(self.text) > 2:
            connection_starter.conn.write('CONNECT', self.text)
            self.board.player.name = self.text
            self.text = ""

    def start_match(self):
        self.is_login = False
        self.board.new()

    def observer_update(self, subject):
        msg = subject.received_msg
        if 'Waiting for an opponent...' in msg:
            self.text_display = False
        if 'OPPONENT:' in msg:
            # print("match is about to start")
            connection_starter.conn.msg_protocol.data.detach_observer(self)
            connection_starter.conn.msg_protocol.data.attach_observer(self.board)
            self.start_match()
        else:
            self.error_msg = msg


login = Login()
connection_starter.conn.msg_protocol.data.attach_observer(login)
connection_thread = threading.Thread(target=connection_starter.connect)

connection_thread.start()  # start connection with the remote server
login.run()  # start display the game

connection_thread.join()


# run through terminal:  python -m PresentationLayer.Login

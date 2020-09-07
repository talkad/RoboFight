import pygame

from PresentationLayer.Game import start_game
from PresentationLayer.Service import screen, background, concat_char, draw_text

# setup pygame
pygame.init()

# generate the chat textbox
name_box = pygame.Rect(150, 370, 600, 40)


class Login:
    def __init__(self):
        self.text = ""
        self.running = True
        self.error_msg = ""

    # Login main loop
    def run(self):
        self.running = True
        while self.running:
            self.events()
            self.update()
            self.draw()

    def update(self):
        pass

    # handle key events
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():

            # add the key to the text
            if event.type == pygame.KEYDOWN:
                self.text = concat_char(self.text, pygame.key.name(event.key))
                if pygame.key.name(event.key) == 'return':
                    self.handle_return()

            # check for closing window
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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
        self.error_msg = "error"
        # if message is ok start board game
        if self.error_msg == 'OK':
            self.running = False
            start_game()
        # else- try again
        else:
            self.text = ""


login = Login()
login.run()

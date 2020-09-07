import pygame

from PresentationLayer.Service import screen, background, concat_char, draw_text

# setup pygame
pygame.init()
pygame.mixer.init()

# generate the chat textbox
name_box = pygame.Rect(150, 370, 600, 40)


class Login:
    def __init__(self):
        self.text = ""
        self.running = True

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
                    self.text = ""

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

        # after drawing everything, flip the display
        pygame.display.flip()


login = Login()
login.run()

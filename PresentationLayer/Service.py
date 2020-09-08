import pygame

from BusinessLayer.Game.Settings import WIDTH, HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.image.load("../img/background.png").convert()
font_name = pygame.font.match_font('arial')


# draw text on screen
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, pygame.Color(color))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def draw_msg_stack(surf, chat, size, color):
    font = pygame.font.Font(font_name, size)
    font.set_bold(5)
    chat_box = last_msg(chat)
    y = 320
    for msg in chat_box:
        text_surface = font.render(msg, True, pygame.Color(color))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (150, y)
        surf.blit(text_surface, text_rect)
        y += 20


def last_msg(chat):
    if len(chat) >= 10:
        return chat[-10:]
    return chat


def remove_first_letter(text):
    length = len(text)
    if length == 0:
        return ""
    elif length == 1:
        return ""
    else:
        return text[1:]


def remove_last_letter(text):
    length = len(text)
    if length == 0:
        return ""
    elif length == 1:
        return ""
    else:
        return text[0: -1]


def concat_char(text, char):
    if char == "backspace":
        text = remove_last_letter(text)
    elif len(text) == 40:  # maximum amount of characters in textbox
        return text
    elif char == "space":
        text += ' '
    elif len(char) != 1:
        pass
    else:
        text += char
    return text


# get the largest number in a given list
def get_max(num_list):
    max_num = -1
    for num in num_list:
        if num > max_num:
            max_num = num
    return max_num


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 150
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, pygame.Color('green'), fill_rect)
    pygame.draw.rect(surf, pygame.Color('white'), outline_rect, 2)

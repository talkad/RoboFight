import pygame
import sys

font_name = pygame.font.match_font('arial')


# draw text on screen
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, pygame.Color(color))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


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
    elif len(text) == 30:  # maximum amount of characters in textbox
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

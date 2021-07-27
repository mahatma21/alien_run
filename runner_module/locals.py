import pygame.font
from pygame.locals import *
import os
import sys

def get_file(*path: str):
    try:
        return join_path(sys._MEIPASS, *path)
    except AttributeError:
        return join_path(*path)

WIN_SIZE = 784, 450
WIN_MID = tuple([n / 2 for n in WIN_SIZE])

join_path = os.path.join

IMG_PATH = join_path('assets', 'images')
PLAYER_PATH = join_path(IMG_PATH, 'player')
SNAIL_PATH = join_path(IMG_PATH, 'snail')
FLY_PATH = join_path(IMG_PATH, 'fly')
AUDIO_PATH = join_path('assets', 'audio')
FONT_PATH = join_path('assets', 'font')

pygame.font.init()
TITLE_FONT = pygame.font.Font(
    get_file(FONT_PATH, 'pixel_type.ttf'), 96)
START_FONT = pygame.font.Font(
    get_file(FONT_PATH, 'pixel_type.ttf'), 36)
SCORE_FONT = pygame.font.Font(
    get_file(FONT_PATH, 'pixel_type.ttf'), 48)
END_SCORE_FONT = pygame.font.Font(
    get_file(FONT_PATH, 'pixel_type.ttf'), 54)

TITLE_TEXT = TITLE_FONT.render("Alien Run", 0, (50, 200, 170))
START_TEXT = START_FONT.render(
    "Press  space  to  start...", 0, Color('black'))
PLAY_AGAIN_TEXT = START_FONT.render(
    "Press space to play again...", 0, Color('black')
)
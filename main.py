import pygame
from pygame.locals import *
import random

pygame.init()

# Create the window
game_width = 800
game_height = 500
screen_size = (game_width, game_height)
game_window = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Side Scroller')
padding_y = 50
import pygame
from pygame.locals import *
import random

pygame.init()

# Create the window
game_width = 800
game_height = 500
screen_size = (game_width, game_height)
game_window = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Space Invaders')
padding_y = 50

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

# Load background image
bg = pygame.image.load('images/bg.png').convert_alpha()
bg = pygame.transform.scale(bg, (game_width, game_height))  # Make sure to scale correctly

# Load sound effects
background_music = pygame.mixer.Sound('sounds/background.ogg')
laser_sound = pygame.mixer.Sound('sounds/laser.wav')
explosion_sound = pygame.mixer.Sound('sounds/explosion.wav')

# Play the background music in a loop
background_music.play(-1)

# Load and scale the airplane images
airplane_images = []
for i in range(3):
    airplane_image = pygame.image.load(f'images/player/fly{i}.png').convert_alpha()
    airplane_images.append(pygame.transform.scale(airplane_image, (200, airplane_image.get_height() * (200 / airplane_image.get_width()))))

# Create sprite groups
player_group = pygame.sprite.Group()

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.lives = 3
        self.images = airplane_images
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move_up(self):
        if self.rect.top > padding_y:
            self.y -= 2
            self.image_index = 1  # Moving up
            return True
        return False

    def move_down(self):
        if self.rect.bottom < game_height - padding_y:
            self.y += 2
            self.image_index = 2  # Moving down
            return True
        return False

    def stop_moving(self):
        self.image_index = 0  # Idle

# Create the player
player = Player(30, game_height // 2)
player_group.add(player)

# Game loop
clock = pygame.time.Clock()
fps = 120
running = True

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Player movement
    if player.lives > 0:
        keys = pygame.key.get_pressed()
        if keys[K_UP]:
            player.move_up()
        elif keys[K_DOWN]:
            player.move_down()
        else:
            player.stop_moving()

        player.update()

    # Draw the background
    game_window.blit(bg, (0, 0))  # Draw the background once at (0, 0)

    # Draw the player
    player_group.update()
    player_group.draw(game_window)

    # Update the display
    pygame.display.flip()

pygame.quit()

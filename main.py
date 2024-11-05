import pygame
from pygame.locals import *
import random

pygame.init()
pygame.mixer.init()

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

# Number of milliseconds before you can fire another bullet
bullet_cooldown = 500

# Timestamp of last bullet fired
last_bullet_time = pygame.time.get_ticks()

# Time when the next enemy ship will spawn
next_enemy_ship = pygame.time.get_ticks()

# Function for resizing an image
def scale_image(image, new_width):
    image_scale = new_width / image.get_rect().width
    new_height = image.get_rect().height * image_scale
    scaled_size = (new_width, new_height)
    return pygame.transform.scale(image, scaled_size)

# Load background image
bg = pygame.image.load('images/bg.png').convert_alpha()
bg = scale_image(bg, game_width)
bg_scroll = 0

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
    airplane_image = scale_image(airplane_image, 200)
    airplane_images.append(airplane_image)

# Load and scale the heart images for representing health
heart_images = []
heart_image_index = 0
for i in range(8):
    heart_image = pygame.image.load(f'images/hearts/heart{i}.png').convert_alpha()
    heart_image = scale_image(heart_image, 30)
    heart_images.append(heart_image)
    
# Load enemy ship images
enemy_ship_images = []
for i in range(5): 
    enemy_ship_image = pygame.image.load(f'images/enemy_ship/enemy{i}.png').convert_alpha()
    enemy_ship_image = scale_image(enemy_ship_image, 50) 
    enemy_ship_images.append(enemy_ship_image)

# Load and scale explosion images
explosion_images = []
for i in range(6):  # Assuming you have 6 explosion images named explosion0, explosion1, ...
    explosion_image = pygame.image.load(f'images/explosion/explosion{i}.png').convert_alpha()
    explosion_image = scale_image(explosion_image, 50)  
    explosion_images.append(explosion_image)
    
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        padding_x = 20  
        self.x = x + padding_x  
        self.y = y
        self.lives = 3
        self.score = 0

        # Use the preloaded and resized airplane images
        self.images = airplane_images  # Reference the resized airplane images here

        # Current image index (0: idle, 1: moving up, 2: moving down)
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = explosion_images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 5
        self.rect = Rect(x, y, 10, 10)

    def draw(self):
        pygame.draw.circle(game_window, yellow, (self.x, self.y), self.radius)
        
class EnemyShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.x = game_width
        self.y = random.randint(padding_y, game_height - padding_y * 2)
        self.image_index = 0
        self.image = enemy_ship_images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    
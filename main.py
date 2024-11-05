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
last_bullet_time = pygame.time.get_ticks()
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
    airplane_image = scale_image(airplane_image, 60)
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
for i in range(6):  
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

        self.images = airplane_images  

        # Current image index (0: idle, 1: moving up, 2: moving down)
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
        self.image_index = 0

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = explosion_images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50  

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                self.kill()  

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.radius = 5
        self.rect = Rect(x, y, 10, 10)

    def draw(self):
        pygame.draw.circle(game_window, yellow, (self.x, self.y), self.radius)

    def update(self):
        self.x += 2
        self.rect.x = self.x
        self.rect.y = self.y
        
        if pygame.sprite.spritecollide(self, enemy_ship_group, True):
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            explosion_sound.play()
            self.kill()
            player.score += 1


        if self.x > game_width:
            self.kill()

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

    def update(self):
        self.x -= 2
        self.image_index += 0.1  
        if self.image_index >= len(enemy_ship_images):
            self.image_index = 0

        self.image = enemy_ship_images[int(self.image_index)]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.rect.x = self.x
        self.rect.y = self.y

        if pygame.sprite.spritecollide(self, bullet_group, True):
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            explosion_sound.play()
            self.kill()
            player.score += 1

        if self.x < 0:
            self.kill()

# Create sprite groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_ship_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

# Create the player
player_x = 30
player_y = game_height // 2
player = Player(player_x, player_y)
player_group.add(player)


# # Game loop
# clock = pygame.time.Clock()
# fps = 120
# running = True

# while running:
#     clock.tick(fps)

#     for event in pygame.event.get():
#         if event.type == QUIT:
#             running = False
            
#     keys = pygame.key.get_pressed()
    
#     # move the airplane using the up/down arrow keys
#     if keys[K_UP] and player.rect.top > padding_y:
#         player.move_up()
#     elif keys[K_DOWN] and player.rect.bottom < game_height - padding_y:
#         player.move_down()
#     else:
#          player.stop_moving()
         
#     # Shoot bullet with space bar
#     if keys[K_SPACE] and last_bullet_time + bullet_cooldown < pygame.time.get_ticks():
#         bullet_x = player.x + player.image.get_width()
#         bullet_y = player.y + player.image.get_height() // 2
#         bullet = Bullet(bullet_x, bullet_y)
#         bullet_group.add(bullet)
#         laser_sound.play()
#         last_bullet_time = pygame.time.get_ticks()
        
#     # Spawn a new enemy ship
#     if next_enemy_ship < pygame.time.get_ticks():
#         enemy_ship = EnemyShip()
#         enemy_ship_group.add(enemy_ship)
#         next_enemy_ship = pygame.time.get_ticks() + random.randint(500, 3000)
        
#     # Bullet-enemy collision and explosion management
#     for bullet in bullet_group:
#         hit_enemy = pygame.sprite.spritecollideany(bullet, enemy_ship_group)
#         if hit_enemy:
#             if not hasattr(hit_enemy, 'destroyed') or not hit_enemy.destroyed:
#                 explosion = Explosion(hit_enemy.rect.centerx, hit_enemy.rect.centery)
#                 explosion_group.add(explosion)
#                 hit_enemy.destroyed = True
#                 hit_enemy.kill()
#                 bullet.kill() 
                
#     # Check for collisions between the player and enemy ships
#     hit_enemy = pygame.sprite.spritecollideany(player, enemy_ship_group)
#     if hit_enemy:
#         # Trigger explosion at the enemy's location and decrement player's life
#         explosion = Explosion(hit_enemy.rect.centerx, hit_enemy.rect.centery)
#         explosion_group.add(explosion)
#         player.lives -= 1  
#         hit_enemy.kill()
        
#     # Draw the background
#     game_window.blit(bg, (0 - bg_scroll, 0))
#     game_window.blit(bg, (game_width - bg_scroll, 0))
#     bg_scroll += 1
#     if bg_scroll == game_width:
#         bg_scroll = 0

#     # Draw the player
#     player_group.update()
#     player_group.draw(game_window)
    
#      # Draw bullets
#     bullet_group.update()
#     for bullet in bullet_group:
#         bullet.draw()

#     # Draw enemy ships
#     enemy_ship_group.update()
#     enemy_ship_group.draw(game_window)

#     # Draw explosions
#     explosion_group.update()
#     explosion_group.draw(game_window)
    
#     # Display remaining lives
#     for i in range(player.lives):
#         heart_image = heart_images[int(heart_image_index)]
#         heart_x = 10 + i * (heart_image.get_width() + 10)
#         heart_y = 10
#         game_window.blit(heart_image, (heart_x, heart_y))
#     heart_image_index = (heart_image_index + 0.1) % len(heart_images)

#     # Display the score
#     font = pygame.font.Font(pygame.font.get_default_font(), 16)
#     text = font.render(f'Score: {player.score}', True, white)
#     text_rect = text.get_rect()
#     text_rect.center = (200, 20)
#     game_window.blit(text, text_rect)
    
#     # Check if game is over and set game_over flag
#     if player.lives == 0:
#         game_over = True
#         background_music.stop()

#     if game_over:
#         # Display "Game Over" message
#         font = pygame.font.Font(pygame.font.get_default_font(), 24)
#         gameover_str = 'Game over. Play again (y or n)?'
#         text = font.render(gameover_str, True, red)
#         text_rect = text.get_rect(center=(game_width / 2, game_height / 2))
#         game_window.blit(text, text_rect)
        
#         # Update display to show the game-over screen
#         pygame.display.flip()

#         # Handle input for restarting or quitting
#         keys = pygame.key.get_pressed()
#         if keys[K_y]:
#             # Restart the game
#             game_over = False
#             player.lives = 3
#             player.score = 0
            
#             # Clear sprite groups
#             player_group.empty()
#             bullet_group.empty()
#             enemy_ship_group.empty()
#             explosion_group.empty()
            
#             # Re-add the player
#             player = Player(player_x, player_y)
#             player_group.add(player)
            
#             # Restart background music
#             background_music.play(-1)
            
#         elif keys[K_n]:
#             running = False
#             break
        
#         pygame.display.flip()

# pygame.quit()

# Game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
    keys = pygame.key.get_pressed()

    # Player movement
    if keys[K_UP]:
        player.move_up()
    elif keys[K_DOWN]:
        player.move_down()
    else:
        player.stop_moving()

    # Shoot bullet with space bar
    if keys[K_SPACE] and last_bullet_time + bullet_cooldown < pygame.time.get_ticks():
        bullet_x = player.x + player.image.get_width()
        bullet_y = player.y + player.image.get_height() // 2
        bullet = Bullet(bullet_x, bullet_y)
        bullet_group.add(bullet)
        last_bullet_time = pygame.time.get_ticks()
        laser_sound.play()

    # Spawn a new enemy ship
    if next_enemy_ship < pygame.time.get_ticks():
        enemy_ship = EnemyShip()
        enemy_ship_group.add(enemy_ship)
        next_enemy_ship = pygame.time.get_ticks() + random.randint(500, 3000)
        
    #Check for collisions between the player and enemy ships
    hit_enemy = pygame.sprite.spritecollideany(player, enemy_ship_group)
    if hit_enemy:
        # Trigger explosion at the enemy's location and decrement player's life
        explosion = Explosion(hit_enemy.rect.centerx, hit_enemy.rect.centery)
        explosion_group.add(explosion)
        player.lives -= 1  
        hit_enemy.kill()  
        
    # Draw the background
    game_window.blit(bg, (0 - bg_scroll, 0))
    game_window.blit(bg, (game_width - bg_scroll, 0))
    bg_scroll += 1
    if bg_scroll == game_width:
        bg_scroll = 0

    # Draw enemy ships
    enemy_ship_group.update()
    enemy_ship_group.draw(game_window)

    # Draw the player
    player_group.update()
    player_group.draw(game_window)

    # Draw bullets
    bullet_group.update()
    for bullet in bullet_group:
        bullet.draw()

    # Draw explosions
    explosion_group.update()
    explosion_group.draw(game_window)

    # Display remaining lives
    for i in range(player.lives):
        heart_image = heart_images[int(heart_image_index)]
        heart_x = 10 + i * (heart_image.get_width() + 10)
        heart_y = 10
        game_window.blit(heart_image, (heart_x, heart_y))
    heart_image_index += 0.1
    
    if heart_image_index >= len(heart_images):
        heart_image_index = 0

    # Display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render(f'Score: {player.score}', True, white)
    text_rect = text.get_rect()
    text_rect.center = (200, 20)
    game_window.blit(text, text_rect)
    
    pygame.display.update()
    
    # Check if game is over
    while player.lives == 0:
        
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        
        gameover_str = f'Game over. Play again (y or n)?'
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        text = font.render(gameover_str, True, red)
        text_rect = text.get_rect()
        text_rect.center = (game_width / 2, game_height / 2)
        game_window.blit(text, text_rect)

        keys = pygame.key.get_pressed()
        if keys[K_y]:

        # clear the sprite groups
            player_group.empty()
            bullet_group.empty()
            enemy_ship_group.empty()

            # reset the player
            player = Player(player_x, player_y)
            player_group.add(player)

        elif keys[K_n]:
            running = False
            break       

    pygame.display.update()

pygame.quit()

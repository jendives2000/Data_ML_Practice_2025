import os
import sys
from random import randint, uniform

import pygame

# ===== Path setup for module import =====
# Get the absolute path of the "app" directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))  # Moves up to 'app/'

# Move up one level to "space-shooter/"
SPACE_SHOOTER_DIR = os.path.dirname(APP_DIR)

# Move up another level to "pygame-ce_python/"
PYGAME_CE_DIR = os.path.dirname(SPACE_SHOOTER_DIR)

# Construct the correct path to "utils-pyg/"
UTILS_PATH = os.path.join(PYGAME_CE_DIR, "utils-pyg")

# Add "utils-pyg" to Python's import path
sys.path.append(UTILS_PATH)

print(f"UTILS_PATH added: {UTILS_PATH}")

from shared_code_pyg import asset_path


# ===== CLASSES WITH SPRITES =====
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(
            asset_path(os.path.join("space-shooter", "images", "player.png"))
        ).convert_alpha()
        self.rect = self.image.get_frect(center=(HALF_WW, HALF_WH * 1.8))
        self.direction = pygame.math.Vector2()
        self.speed = 300

        # cooldown
        self.can_shoot = True
        self.laser_shoot_delay = 0
        self.laser_cooldown = 400

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_delay >= self.laser_cooldown:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # making diagonal moves same speed as horizontal/vertical moves
        self.direction = (
            self.direction.normalize() if self.direction else self.direction
        )
        # movement:
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, all_sprites)
            print("fire laser")
            self.can_shoot = False
            self.laser_shoot_delay = pygame.time.get_ticks()

        self.laser_timer()


class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(
            center=(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT))
        )


class Laser(pygame.sprite.Sprite):
    def __init__(self, laser_itself, laser_pos, groups):
        super().__init__(groups)
        self.image = laser_itself
        self.rect = self.image.get_frect(midbottom=laser_pos)

    def update(self, dt):
        # make the laser move upward
        self.rect.centery -= 400 * dt

        # kill the laser instance once it's out screen:
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):
    def __init__(self, meteor_itself, meteor_pos, groups):
        super().__init__(groups)
        self.image = meteor_itself
        self.rect = self.image.get_frect(center=meteor_pos)
        self.timer = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.timer >= self.lifetime:
            self.kill()


# ===== GENERAL SETUP =====
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
HALF_WW, HALF_WH = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
display_surface = pygame.display.set_caption("Speed Asteroids")
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()

# ===== IMPORTING ASSETS =====
# import one Star...
star_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "star.png"))
).convert_alpha()
# Meteor:
meteor_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "meteor.png"))
).convert_alpha()
# Laser:
laser_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "laser.png"))
).convert_alpha()

# Sprites
all_sprites = pygame.sprite.Group()
# use it 25 times
for i in range(25):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom events -> meteor event
meteor_spawn = pygame.event.custom_type()
pygame.time.set_timer(meteor_spawn, 500)

# ===== GAME LOOP =====
while running:
    # delta time in seconds:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_spawn:
            x, y = randint(0, WINDOW_WIDTH), randint(-200, -100)
            Meteor(meteor_surf, (x, y), all_sprites)

    # update
    all_sprites.update(dt)

    # draw the game, first at the bottom, last on top of all
    display_surface.fill("grey12")

    # meteor_surf:
    # display_surface.blit(meteor_surf, meteor_rect)
    # laser_surf:
    # display_surface.blit(laser_surf, laser_rect)
    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()

import os
import sys
from random import randint

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
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            asset_path(os.path.join("space-shooter", "images", "player.png"))
        ).convert_alpha()
        self.rect = self.image.get_frect(center=(HALF_WW, HALF_WH * 1.8))


# ===== general setup =====
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
HALF_WW, HALF_WH = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
display_surface = pygame.display.set_caption("Speed Asteroids")
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
clock = pygame.time.Clock()

# plain surface, own dimensions
surf = pygame.Surface((100, 200))
surf.fill("white")
x = 100

player = Player()

# ===== IMPORTING ASSETS =====
# player graph asset:
# player_surf = pygame.image.load(
#     asset_path(os.path.join("space-shooter", "images", "player.png"))
# ).convert_alpha()
# player_rect = player_surf.get_frect(center=(HALF_WW, HALF_WH * 1.8))
# # direction: 1 means left & right is possible, 0 means up & down is impossible
# player_direction = pygame.math.Vector2()
# player_speed = 300

# Star asset
star_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "star.png"))
).convert_alpha()
star_positions = [
    (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(20)
]

# Meteor:
meteor_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "meteor.png"))
).convert_alpha()
meteor_rect = meteor_surf.get_frect(center=(HALF_WW, HALF_WH))

laser_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "laser.png"))
).convert_alpha()
laser_rect = laser_surf.get_frect(bottomleft=(20, WINDOW_HEIGHT - 20))


# ===== GAME LOOP =====
while running:
    # delta time in seconds:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.KEYDOWN and event.type == pygame.K_1:
        #     print(1)
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos

    # input
    # keys = pygame.key.get_pressed()
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # # making diagonal moves same speed as horizontal/vertical moves
    # player_direction = (
    #     player_direction.normalize() if player_direction else player_direction
    # )
    # # movement:
    # player_rect.center += player_direction * player_speed * dt

    # draw the game, first at the bottom, last on top of all
    display_surface.fill("grey12")
    # placing 20 stars randomly:
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    # meteor_surf:
    display_surface.blit(meteor_surf, meteor_rect)
    # laser_surf:
    display_surface.blit(laser_surf, laser_rect)

    # player_surf:
    # display_surface.blit(player_surf, player_rect)
    display_surface.blit(player.image, player.rect)

    pygame.display.update()

pygame.quit()

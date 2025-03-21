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

# ===== IMPORTING ASSETS =====
# player graph asset:
player_surf = pygame.image.load(
    asset_path(os.path.join("space-shooter", "images", "player.png"))
).convert_alpha()
player_rect = player_surf.get_frect(center=(HALF_WW, HALF_WH * 1.8))
player_direction = pygame.math.Vector2(2, -1)
player_speed = 10

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
    clock.tick(10)
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game, first at the bottom, last on top of all
    display_surface.fill("grey12")
    # placing 20 stars randomly:
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    # meteor_surf:
    display_surface.blit(meteor_surf, meteor_rect)
    # laser_surf:
    display_surface.blit(laser_surf, laser_rect)
    # bouncing player from RIGHT side to LEFT:
    player_rect.center += player_direction * player_speed
    # player_surf:
    display_surface.blit(player_surf, player_rect)

    pygame.display.update()

pygame.quit()

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
display_surface = pygame.display.set_caption("Speed Asteroids")
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True

# plain surface, own dimensions
surf = pygame.Surface((100, 200))
surf.fill("white")
x = 100

# importing the player graph asset:
player_surf = pygame.image.load(
    asset_path("space-shooter/images/player.png")
).convert_alpha()

# importing star asset:
star_surf = pygame.image.load(
    asset_path("space-shooter/images/star.png")
).convert_alpha()
star_positions = [
    (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(20)
]

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # draw the game, first at the bottom, last on top of all
    display_surface.fill("grey12")
    # placing 20 stars randomly:
    for pos in star_positions:
        display_surface.blit(star_surf, pos)
    # surface own position relative to origin (top left corner):
    display_surface.blit(player_surf, (x, 150))

    pygame.display.update()

pygame.quit()

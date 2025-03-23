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
        self.rotation = 0

        # cooldown
        self.can_shoot = True
        self.laser_shoot_delay = 0
        self.laser_cooldown = 280

        # mask:
        mask = pygame.mask.from_surface(self.image)

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
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_delay = pygame.time.get_ticks()
            laser_wav.play()

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
        self.original_surf = meteor_itself
        self.image = meteor_itself
        self.rect = self.image.get_frect(center=meteor_pos)
        self.timer = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.4, 0.4), 1)
        self.speed = randint(300, 550)
        self.rotation_speed = randint(-110, 110)
        self.rotation = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.timer >= self.lifetime:
            self.kill()

        # rotating:
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(
            self.original_surf, self.rotation, scale=1
        )
        self.rect = self.image.get_frect(center=self.rect.center)


class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=pos)

    def update(self, dt):
        self.frame_index += 20 * dt  # results in float, so needs int wrapper
        # continuous explosions
        # self.image = self.frames[int(self.frame_index) % len(self.frames)]
        # explosions just once:
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()


class SpeedCapsule(pygame.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(*groups)
        text = "Speed"
        font = pygame.font.Font(None, 16)
        text_surf = font.render(text, True, "yellow")
        padding = 5
        frame_rect = text_surf.get_rect().inflate(padding * 2, padding * 2)
        self.image = pygame.Surface(frame_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            "yellow",
            self.image.get_rect(),
            width=2,
            border_radius=frame_rect.height // 2,
        )
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surf, text_rect)

        self.rect = self.image.get_rect(center=pos)
        # Store the position as a float using a Vector2.
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 170  # pixels per second

    def update(self, dt):
        # Update the float position
        self.pos.y += self.speed * dt
        # Update the rect using the float position
        self.rect.centery = int(self.pos.y)
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()


score_count = 0


def collisions():
    global running, score_count

    # collisions player/meteor, dokill is on meteor_sprites not player:
    collision_1 = pygame.sprite.spritecollide(
        player, meteor_sprites, dokill=True, collided=pygame.sprite.collide_mask
    )
    if collision_1:
        running = False
    # collision laser / meteor:
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(
            laser, meteor_sprites, dokill=True
        )
        if collided_sprites:
            laser.kill()
            # instance of class object explosions:
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            # explosion sound:
            explosion_wav.play()
            score_count += 1
            # 20% chance to spawn a capsule at the explosion location
            if randint(1, 100) <= 5:
                SpeedCapsule(laser.rect.midtop, all_sprites, capsule_sprites)

    # Collision: player/capsule (increase player speed)
    capsule_hits = pygame.sprite.spritecollide(player, capsule_sprites, dokill=True)
    if capsule_hits:
        # Increase the player's speed by 50 each time a capsule is collected.
        player.speed += 50
        speedup_wav.play()


color = (230, 230, 230)


def display_playtime():
    current_time = pygame.time.get_ticks()
    text_surf: pygame.Surface = font.render(
        text=str(current_time), antialias=True, color=color
    )
    text_rect = text_surf.get_frect(midbottom=(75, 75))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(
        display_surface,
        color=color,
        rect=text_rect.inflate(20, 10).move(0, -8),
        border_radius=10,
        width=5,
    )


def display_score(score_count):
    text_surf: pygame.Surface = font.render(
        text=str(score_count), antialias=True, color="green"
    )
    text_rect = text_surf.get_frect(midbottom=(210, 75))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(
        display_surface,
        color="green",
        rect=text_rect.inflate(20, 10).move(0, -8),
        border_radius=10,
        width=5,
    )


def display_instructions():
    instruction_text = (
        "========== MOVE ==========\n\n"
        "LEFT, RIGHT, UP, DOWN\n\n"
        "========== SHOT ==========\n\n"
        "SPACEBAR\n\n"
        "ENTER or ESC to skip"
    )

    # Load font with emoji support (fallback to default if needed)
    font = pygame.font.SysFont("Courier New", 28)  # Windows
    # font = pygame.font.SysFont("Noto Color Emoji", 32)  # Linux

    # Render multiline text (pygame doesn't support it natively)
    lines = instruction_text.split("\n")
    surfaces = [font.render(line, True, (200, 200, 200)) for line in lines]

    # Compute total height
    total_height = sum(s.get_height() for s in surfaces)
    max_width = max(s.get_width() for s in surfaces)

    # Create the rect
    padding = 25
    box_rect = pygame.Rect(0, 0, max_width + padding * 2, total_height + padding * 2)
    box_rect.center = (HALF_WW, HALF_WH)

    # Draw the border rectangle
    pygame.draw.rect(
        display_surface,
        color=(200, 200, 200),
        rect=box_rect,
        border_radius=3,
        width=5,
    )

    # Blit each line with vertical spacing
    y_offset = box_rect.top + padding
    for surf in surfaces:
        line_rect = surf.get_rect(centerx=box_rect.centerx, top=y_offset)
        display_surface.blit(surf, line_rect)
        y_offset += surf.get_height()


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
# Font for text:
font = pygame.font.Font(
    asset_path(os.path.join("space-shooter", "images", "Oxanium-Bold.ttf")), size=40
)
# explosion frames:
explosion_frames = [
    pygame.image.load(
        asset_path(os.path.join("space-shooter", "images", "explosions", f"{i}.png"))
    ).convert_alpha()
    for i in range(21)
]

# sounds:
laser_wav = pygame.mixer.Sound(
    asset_path(os.path.join("space-shooter", "audio", "laser.wav"))
)
laser_wav.set_volume(0.20)
explosion_wav = pygame.mixer.Sound(
    asset_path(os.path.join("space-shooter", "audio", "explosion.wav"))
)
explosion_wav.set_volume(0.22)
damage_wav = pygame.mixer.Sound(
    asset_path(os.path.join("space-shooter", "audio", "damage.ogg"))
)
game_music_wav = pygame.mixer.Sound(
    asset_path(os.path.join("space-shooter", "audio", "Speed_Asteroids.mp3"))
)
game_music_wav.set_volume(0.42)
speedup_wav = pygame.mixer.Sound(
    asset_path(os.path.join("space-shooter", "audio", "speedup.wav"))
)
speedup_wav.set_volume(0.3)


# Sprites
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
capsule_sprites = pygame.sprite.Group()
# use it 25 times
for i in range(25):
    Star(all_sprites, star_surf)
player = Player(all_sprites)


# custom events -> meteor event
spawn_interval = 300
thresholds = [23000, 59000, 127000, 158000, 229000]
meteor_spawn = pygame.event.custom_type()
# smaller the time, the more spawns
pygame.time.set_timer(meteor_spawn, spawn_interval)


# ===== INSTRUCTIONS DISPLAY =====
# Display instructions for 5 seconds before starting the game
instructions_duration = 5000  # milliseconds
start_time = pygame.time.get_ticks()

while True:
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                # Skip the intro if Enter or Esc is pressed
                break

    # Fill the screen and display the instructions
    display_surface.fill("black")
    display_instructions()
    pygame.display.update()

    # Break out after 5 seconds
    if current_time - start_time >= instructions_duration:
        break

game_music_wav.play(loops=-1)

# Enable input after intro
pygame.event.set_allowed(None)

# ===== GAME LOOP =====
while running:
    # delta time in seconds:
    dt = clock.tick() / 1000
    current_time = pygame.time.get_ticks()  # elapsed time in ms

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_spawn:
            x, y = randint(250, WINDOW_WIDTH - 250), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))

    # Check if it's time to increase the spawn interval
    if current_time == thresholds[0]:
        # Increase interval by 30%
        spawn_interval = int(spawn_interval * 1.3)
        pygame.time.set_timer(meteor_spawn, spawn_interval)
        # Remove the threshold we just passed so that thresholds[0] becomes the next threshold
        thresholds.pop(0)

    # update
    all_sprites.update(dt)
    collisions()

    # draw the game, first at the bottom, last on top of all
    display_surface.fill("grey16")
    all_sprites.draw(display_surface)
    display_playtime()
    display_score(score_count)

    pygame.display.update()

pygame.quit()

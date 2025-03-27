import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Jumpy Yay!"
TILE_SCALING = 0.5
GRAVITY = 1
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 20


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.wall_list = None

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        self.background_color = arcade.csscolor.DODGER_BLUE

        # === PLAYER ===
        self.player_texture = arcade.load_texture(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        )
        self.player_sprite = arcade.Sprite(
            self.player_texture,
            center_x=64,
            center_y=128,
        )
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player_sprite)

        # === WALLS ===
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", scale=TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)

        # === PHYSICS ENGINE ===
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.wall_list, gravity_constant=GRAVITY
        )

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        # Code to draw other things will go here
        arcade.draw_sprite(self.player_sprite)

        self.player_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        self.physics_engine.update()

    # TRIGGERING MOVEMENTS
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        if key == arcade.key.ESCAPE:
            self.setup()

    # STOPPING TRIGGERING MOVEMENTS
    def on_key_release(self, key, modifiers):
        """Called whenever a key is released."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

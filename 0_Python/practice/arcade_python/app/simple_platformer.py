import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Jumpy Yay!"
TILE_SCALING = 0.5
COIN_SCALING = 0.5
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

        self.scene = None
        self.tile_map = None

        self.player_texture = None
        self.player_sprite = None
        self.camera = None

        # # === SCORE CARD ===
        self.gui_camera = None
        self.score = 0
        self.score_text = None

        # === SOUNDS ===
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.gameover_sound = arcade.load_sound(":resources:sounds/gameover1.wav")

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        layer_options = {"Platforms": {"use_spatial_hash": True}}

        self.tile_map = arcade.load_tilemap(
            ":resources:tiled_maps/map2_level_1.json",
            scaling=TILE_SCALING,
            layer_options=layer_options,
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # === PLAYER ===
        self.scene.add_sprite_list_after("Player", "Foreground")
        self.player_texture = arcade.load_texture(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        )
        self.player_sprite = arcade.Sprite(
            self.player_texture,
            center_x=64,
            center_y=128,
        )
        self.scene.add_sprite("Player", self.player_sprite)

        # === COINS ===

        # === SCORE ===
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.score = 0
        self.score_text = arcade.Text(f"SCORE: {self.score}", x=0, y=5)

        # === WALLS ===

        # Add coins to the world

        # === PHYSICS ENGINE ===
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Platforms"], gravity_constant=GRAVITY
        )

        self.background_color = arcade.csscolor.DODGER_BLUE

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        self.camera.use()

        # Code to draw other things will go here
        arcade.draw_sprite(self.player_sprite)

        self.scene.draw()

        # Activate our GUI camera
        self.gui_camera.use()

        # Draw our Score
        self.score_text.draw()

    def on_update(self, delta_time):
        """Movement and Game Logic"""

        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"SCORE: {self.score}"

        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Don't Touch"]
        ):
            arcade.play_sound(self.gameover_sound)
            self.setup()

        self.camera.position = self.player_sprite.position

    # TRIGGERING MOVEMENTS
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
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

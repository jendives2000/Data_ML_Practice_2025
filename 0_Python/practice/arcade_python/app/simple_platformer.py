import arcade

# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Jumpy Doo"


class GameView(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class to set up the window
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.background_color = arcade.csscolor.DODGER_BLUE

        self.player_texture = arcade.load_texture(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        )
        self.player_sprite = arcade.Sprite(
            self.player_texture,
            scale=2,
            center_x=400,
            center_y=400,
        )
        # self.player_sprite.center_x = 64
        # self.player_sprite.center_y = 128

    def on_resize(self, width, height):
        """This method is automatically called when the window is resized."""

        # Call the parent. Failing to do this will mess up the coordinates,
        # and default to 0,0 at the center and the edges being -1 to 1.
        super().on_resize(width, height)

        print(f"Window resized to: {width}, {height}")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        # The clear method should always be called at the start of on_draw.
        # It clears the whole screen to whatever the background color is
        # set to. This ensures that you have a clean slate for drawing each
        # frame of the game.
        self.clear()

        # Code to draw other things will go here
        arcade.draw_sprite(self.player_sprite)


def main():
    """Main function"""
    # Create a window class. This is what actually shows up on screen
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)

    window = GameView()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

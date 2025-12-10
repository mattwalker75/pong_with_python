"""Main entry point for the Pong game."""
import arcade
from game.settings import settings
from game.ui.main_menu import MainMenuView
from game.ui.settings_menu import SettingsMenuView
from game.pong_window import PongGameView


def main() -> None:
    """Run the Pong game."""
    # Create window
    window = arcade.Window(
        settings.screen_width,
        settings.screen_height,
        settings.screen_title,
        resizable=True,
        update_rate=1 / settings.target_fps
    )

    # Create main menu
    menu = MainMenuView()

    # Set up menu callbacks
    def start_single_player() -> None:
        """Start single player game."""
        game_view = PongGameView("single")
        game_view.setup()
        window.show_view(game_view)

    def start_two_player() -> None:
        """Start two player game."""
        game_view = PongGameView("two_player")
        game_view.setup()
        window.show_view(game_view)

    def show_settings() -> None:
        """Show settings menu."""
        settings_view = SettingsMenuView()
        settings_view.on_back = lambda: window.show_view(menu)
        settings_view.setup()
        window.show_view(settings_view)

    def quit_game() -> None:
        """Quit the game."""
        window.close()

    menu.on_single_player = start_single_player
    menu.on_two_player = start_two_player
    menu.on_settings = show_settings
    menu.on_quit = quit_game

    # Show menu and run
    menu.setup()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()

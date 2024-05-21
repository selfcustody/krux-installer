from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.warning_beta_screen import WarningBetaScreen


class TestSelectVersionScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WarningBetaScreen")
        self.assertEqual(screen.id, "warning_beta_screen")
        self.assertEqual(grid.id, "warning_beta_screen_grid")
        self.assertEqual(button.id, "warning_beta_screen_warn")

        text = [
            "[size=32sp][color=#efcc00][b]WARNING[/b][/color][/size]",
            "",
            "[size=20sp][color=#efcc00]This is our test repository[/color][/size]",
            "",
            "[size=16sp]These are unsigned binaries for the latest and most experimental features[/size]",
            "[size=16sp]and it's just for trying new things and providing feedback.[/size]",
        ]
        self.assertEqual(button.text, "\n".join(text))
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.warning_beta_screen.WarningBetaScreen.set_background")
    def test_on_press(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_press_warning_beta_screen_warn")
        action(button)

        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.warning_beta_screen.WarningBetaScreen.set_background")
    @patch("src.app.screens.warning_beta_screen.WarningBetaScreen.set_screen")
    def test_on_release(
        self, mock_set_screen, mock_set_background, mock_get_running_app
    ):

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_release_warning_beta_screen_warn")
        action(button)
        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 0))
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")
        mock_get_running_app.assert_called_once()

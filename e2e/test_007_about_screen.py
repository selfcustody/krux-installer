from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.about_screen import AboutScreen


class TestAboutScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "AboutScreen")
        self.assertEqual(screen.id, "about_screen")
        self.assertEqual(grid.id, "about_screen_grid")
        self.assertEqual(button.id, "about_screen_button")

        title = "[b]krux-installer[/b]"
        version = "v0.0.2"
        source = "[color=#00AABB][ref=https://github.com/selfcustody/krux-installer]Check source code[/ref][/color]"
        issues = "[color=#00AABB][ref=https://github.com/selfcustody/krux-installer/issues]I found a bug![/ref][/color]"

        self.assertEqual(
            button.text, "\n".join([title, version, "", source, "", issues])
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.about_screen.AboutScreen.set_background")
    def test_on_press(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_press_about_screen_button")
        action(button)

        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.about_screen.AboutScreen.set_background")
    @patch("src.app.screens.about_screen.AboutScreen.set_screen")
    def test_on_release(
        self, mock_set_screen, mock_set_background, mock_get_running_app
    ):

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_release_about_screen_button")
        action(button)

        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 0))
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.about_screen.webbrowser.open")
    def test_on_ref_press(self, mock_webbrowser_open, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_ref_press_about_screen_button")
        action(button, "https://mock.test")

        mock_get_running_app.assert_called_once()
        mock_webbrowser_open.assert_called_once_with("https://mock.test")

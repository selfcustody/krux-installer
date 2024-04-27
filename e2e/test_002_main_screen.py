from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.main_screen import MainScreen


class TestMainScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "MainScreen")
        self.assertEqual(screen.id, "main_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.on_press")
    def test_before_goto_screen_flash(self, mock_on_press):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="FlashScreen")
        mock_on_press.assert_called_once_with(wid="main_flash_device")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.on_release")
    def test_goto_screen_flash(self, mock_on_release, mock_set_screen):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="FlashScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="main_flash_device")
        mock_set_screen.assert_called_once_with(name="FlashScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.on_press")
    def test_before_goto_screen_wipe(self, mock_on_press):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="WipeScreen")
        mock_on_press.assert_called_once_with(wid="main_wipe_device")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.on_release")
    def test_goto_screen_wipe(self, mock_on_release, mock_set_screen):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="WipeScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="main_wipe_device")
        mock_set_screen.assert_called_once_with(name="WipeScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.on_press")
    def test_before_goto_screen_settings(self, mock_on_press):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="SettingsScreen")
        mock_on_press.assert_called_once_with(wid="main_settings")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.on_release")
    def test_goto_screen_settings(self, mock_on_release, mock_set_screen):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="SettingsScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="main_settings")
        mock_set_screen.assert_called_once_with(name="SettingsScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.on_press")
    def test_before_goto_screen_about(self, mock_on_press):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="AboutScreen")
        mock_on_press.assert_called_once_with(wid="main_about")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.on_release")
    def test_goto_screen_about(self, mock_on_release, mock_set_screen):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="AboutScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="main_about")
        mock_set_screen.assert_called_once_with(name="AboutScreen", direction="left")

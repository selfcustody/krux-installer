from unittest.mock import patch, call
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
    @patch("src.app.screens.main_screen.MainScreen.make_on_press")
    def test_make_on_press(self, mock_make_on_press):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_make_on_press.assert_has_calls(
            [
                call(wid="main_select_device"),
                call(wid="main_select_version"),
                call(wid="main_flash"),
                call(wid="main_wipe"),
                call(wid="main_settings"),
                call(wid="main_about"),
            ]
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.make_on_release")
    def test_make_on_release(self, mock_make_on_release):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_make_on_release.assert_has_calls(
            [
                call(wid="main_select_device"),
                call(wid="main_select_version"),
                call(wid="main_flash"),
                call(wid="main_wipe"),
                call(wid="main_settings"),
                call(wid="main_about"),
            ]
        )

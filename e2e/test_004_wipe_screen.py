from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.wipe_screen import WipeScreen


class TestWipeScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WipeScreen")
        self.assertEqual(screen.id, "wipe_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.wipe_screen.WipeScreen.on_press")
    def test_before_goto_screen_select_device(self, mock_on_press):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.before_goto_screen(name="SelectDeviceScreen")
        mock_on_press.assert_called_once_with(wid="flash_select_device")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.wipe_screen.WipeScreen.set_screen")
    @patch("src.app.screens.wipe_screen.WipeScreen.on_release")
    def test_goto_screen_select_device(self, mock_on_release, mock_set_screen):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.goto_screen(name="SelectDeviceScreen", direction="left")
        mock_on_release.assert_called_once_with(wid="flash_select_device")
        mock_set_screen.assert_called_once_with(
            name="SelectDeviceScreen", direction="left"
        )

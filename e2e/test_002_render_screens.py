from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app import MainScreen
from src.app import FlashScreen
from src.app import WipeScreen
from src.app import SettingsScreen


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
    def test_render_flash_screen(self):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "FlashScreen")
        self.assertEqual(screen.id, "flash_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_wipe_screen(self):
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
    def test_render_settings_screen(self):
        screen = SettingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SettingsScreen")
        self.assertEqual(screen.id, "settings_screen")

from kivy.base import EventLoop
from kivy.tests.common import GraphicUnitTest
from src.app import FlashScreen


class TestFlashScreen(GraphicUnitTest):

    def test_render(self):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "FlashScreen")
        self.assertEqual(screen.id, "flash_screen")

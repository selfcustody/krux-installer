from kivy.base import EventLoop
from kivy.tests.common import GraphicUnitTest
from src.app import WipeScreen


class TestWipeScreen(GraphicUnitTest):

    def test_render(self):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WipeScreen")
        self.assertEqual(screen.id, "wipe_screen")

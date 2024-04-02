from kivy.base import EventLoop
from kivy.tests.common import GraphicUnitTest
from src.app import MainScreen


class TestMainScreen(GraphicUnitTest):

    def test_render(self):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "MainScreen")
        self.assertEqual(screen.id, "main_screen")

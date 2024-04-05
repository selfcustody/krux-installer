from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from src.app.base_screen import BaseScreen


class TestBaseScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render(self):
        screen = BaseScreen(wid="mock", name="Mock")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(window.children[0].height, window.height)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_set_background(self):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.ids = {}
        screen.ids["mocked_button"] = Button()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        screen.set_background(wid="mocked_button", rgba=(0, 0, 0, 0))

        # your asserts
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[0], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[1], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[2], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[3], 0)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_on_press(self):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.ids = {}
        screen.ids["mocked_button"] = Button()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        screen.on_press(wid="mocked_button")

        # your asserts
        self.assertEqual(
            window.children[0].ids["mocked_button"].background_color[0], 0.5
        )
        self.assertEqual(
            window.children[0].ids["mocked_button"].background_color[1], 0.5
        )
        self.assertEqual(
            window.children[0].ids["mocked_button"].background_color[2], 0.5
        )
        self.assertEqual(
            window.children[0].ids["mocked_button"].background_color[3], 0.5
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_on_release(self):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.ids = {}
        screen.ids["mocked_button"] = Button()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        screen.on_release(wid="mocked_button")

        # your asserts
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[0], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[1], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[2], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[3], 0)

    def test_set_screen(self):
        screen_manager = ScreenManager()
        screen_0 = BaseScreen(wid="mock_0", name="Mock_0")
        screen_1 = BaseScreen(wid="mock_1", name="Mock_1")

        screen_manager.add_widget(screen_0)
        screen_manager.add_widget(screen_1)
        self.render(screen_manager)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(screen_manager.current, "Mock_0")

        screen_0.set_screen(name="Mock_1", direction="left")
        self.assertEqual(screen_manager.current, "Mock_1")

        screen_1.set_screen(name="Mock_0", direction="right")
        self.assertEqual(screen_manager.current, "Mock_0")

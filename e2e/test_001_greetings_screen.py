import os
from pathlib import Path
from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.greetings_screen import GreetingsScreen


class TestAboutScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen_only_logo(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        image = grid.children[0]

        # default assertions
        root = Path(__file__).parent.parent
        assets = os.path.join(root, "assets", "logo.png")
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "GreetingsScreen")
        self.assertEqual(screen.id, "greetings_screen")
        self.assertEqual(image.source, assets)

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_fail_invalid_name(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="Mock")

        self.assertEqual(str(exc_info.exception), "Invalid screen: Mock")

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_fail_invalid_key(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="GreetingsScreen", key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid key: 'mock'")

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_fail_invalid_value_none(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="GreetingsScreen", key="change_screen", value=None)

        # default assertions
        self.assertEqual(
            str(exc_info.exception), "Invalid value for 'change_screen': None"
        )

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_fail_invalid_value(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="GreetingsScreen", key="change_screen", value="mock")

        # default assertions
        self.assertEqual(
            str(exc_info.exception), "Invalid value for 'change_screen': mock"
        )

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_screen")
    def test_update_change_screen_to_main_screen(
        self, mock_set_screen, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(name="GreetingsScreen", key="change_screen", value="MainScreen")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_screen")
    def test_update_change_screen_to_check_permissions_screen(
        self, mock_set_screen, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(
            name="GreetingsScreen", key="change_screen", value="CheckPermissionsScreen"
        )

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_screen.assert_called_once_with(
            name="CheckPermissionsScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.Color")
    @patch("src.app.screens.greetings_screen.Rectangle")
    def test_update_canvas(self, mock_rectangle, mock_color, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(name="GreetingsScreen", key="canvas")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_color.assert_called_once_with(0, 0, 0)
        mock_rectangle.assert_called_once_with(pos=(0, 0), size=(1600, 1200))

    @patch("sys.platform", "linux")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_update_check_permissions_linux(
        self, mock_schedule_once, mock_partial, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(name="GreetingsScreen", key="check_permissions")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    screen.update,
                    name=screen.name,
                    key="change_screen",
                    value="CheckPermissionsScreen",
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 2.1)]
        )

    @patch("sys.platform", "darwin")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_update_check_permissions_darwin(
        self, mock_schedule_once, mock_partial, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(name="GreetingsScreen", key="check_permissions")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    screen.update,
                    name=screen.name,
                    key="change_screen",
                    value="MainScreen",
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 2.1)]
        )

    @patch("sys.platform", "win32")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_update_check_permissions_win32(
        self, mock_schedule_once, mock_partial, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(name="GreetingsScreen", key="check_permissions")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    screen.update,
                    name=screen.name,
                    key="change_screen",
                    value="MainScreen",
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 2.1)]
        )

    @patch("sys.platform", "mockos")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_fail_update_check_permissions_wrong_os(
        self, mock_schedule_once, mock_partial, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(RuntimeError) as exc_info:
            screen.update(name="GreetingsScreen", key="check_permissions")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Not implemented for mockos")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_partial.assert_called_once_with(
            screen.update, name=screen.name, key="canvas"
        )
        mock_schedule_once.assert_not_called()

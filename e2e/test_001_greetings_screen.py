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
        button = grid.children[0]

        # default assertions
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "GreetingsScreen")
        self.assertEqual(screen.id, "greetings_screen")

        text = "\n".join(
            [
                "     ██           ",
                "     ██           ",
                "     ██           ",
                "   ██████         ",
                "     ██           ",
                "       ██   ██       ",
                "       ██  ██        ",
                "      ████         ",
                "       ██  ██        ",
                "       ██   ██       ",
                "       ██    ██      ",
                "                    ",
                "   KRUX INSTALLER   ",
            ]
        )

        self.assertEqual(button.text, text)

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
    def test_change_to_main_screen(self, mock_set_screen, mock_get_running_app):
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
    def test_change_to_check_permissions_screen(
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
    @patch("sys.platform", "mockos")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    def test_on_enter_fail(self, mock_partial, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        with self.assertRaises(RuntimeError) as exc_info:
            screen.on_enter()

        # default assertions
        self.assertEqual(str(exc_info.exception), "Not implemented for mockos")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        assert not mock_partial.called

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    def test_on_enter_in_linux(self, mock_partial, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        screen.on_enter()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_partial.assert_called_with(
            screen.update,
            name=screen.name,
            key="change_screen",
            value="CheckPermissionsScreen",
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "darwin")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    def test_on_enter_in_darwin(self, mock_partial, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        screen.on_enter()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_partial.assert_called_with(
            screen.update, name=screen.name, key="change_screen", value="MainScreen"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "win32")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    def test_on_enter_in_win32(self, mock_partial, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        screen.on_enter()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_partial.assert_called_with(
            screen.update, name=screen.name, key="change_screen", value="MainScreen"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_background")
    def test_press_button(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        action = getattr(screen, "on_press_greetings_screen_button")
        action(button)

        # patch assertions
        mock_set_background.assert_called_once_with(
            wid="greetings_screen_button", rgba=(0.25, 0.25, 0.25, 1)
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_background")
    def test_release_button(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        action = getattr(screen, "on_release_greetings_screen_button")
        action(button)

        # patch assertions
        mock_set_background.assert_called_once_with(
            wid="greetings_screen_button", rgba=(0, 0, 0, 1)
        )
        mock_get_running_app.assert_called_once()

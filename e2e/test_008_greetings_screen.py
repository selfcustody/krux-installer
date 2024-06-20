from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.greetings_screen import GreetingsScreen


class TestAboutScreen(GraphicUnitTest):

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
        self.assertEqual(screen.bin, None)
        self.assertEqual(screen.bin_args, None)
        self.assertEqual(screen.user, None)
        self.assertEqual(screen.in_dialout, False)

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
    def test_render_main_screen_update_fail_invalid_name(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="Mock", key=None)

        self.assertEqual(str(exc_info.exception), "Invalid screen: Mock")

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen_update_fail_invalid_key(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="ConfigKruxInstaller", key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid key: 'mock'")

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen_update_fail_change_screen_none(
        self, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="ConfigKruxInstaller", key="change_screen", value=None)

        # default assertions
        self.assertEqual(
            str(exc_info.exception), "Invalid value for 'change_screen': None"
        )

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen_update_fail_change_screen_not_in(
        self, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(
                name="ConfigKruxInstaller", key="change_screen", value="MockScreen"
            )

        # default assertions
        self.assertEqual(
            str(exc_info.exception), "Invalid value for 'change_screen': MockScreen"
        )

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_render_main_screen_update_change_screen_main(
        self, mock_set_screen, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        screen.update(
            name="ConfigKruxInstaller", key="change_screen", value="MainScreen"
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen_update_skip_permission_message(
        self, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do the tests
        screen.update(name="GreetingsScreen", key="skip_permission_message")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.distro.name", return_value="MockOS")
    def test_render_main_screen_update_show_permission_message(
        self, mock_distro, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-b"]
        screen.group = "group"
        screen.user = "user"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        screen.update(name="GreetingsScreen", key="show_permission_message")
        message = "\n".join(
            [
                "[size=32sp][color=#efcc00]WARNING[/color][/size]",
                "",
                '[size=16sp]This is the first run of KruxInstaller in "MockOS"',
                "and it appears that you do not have privileged access to make flash procedures.",
                "To proceed, click in the screen and a prompt will ask for your password",
                "to execute the following command:",
                "[color=#00ff00]mock -a -b group user[/color][/size]",
            ]
        )
        self.assertEqual(button.text, message)
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_distro.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockeduser")
    @patch("src.app.screens.greetings_screen.distro.id", return_value="mockos")
    @patch("src.app.screens.greetings_screen.distro.like", return_value="mockos")
    @patch("src.app.screens.greetings_screen.distro.name", return_value="mockos")
    def test_render_main_screen_update_fail_check_user(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        with self.assertRaises(RuntimeError) as exc_info:
            screen.update(name="GreetingsScreen", key="check_user")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Not implemented for 'mockos'")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_environ_get.assert_called_once_with("USER")
        mock_name.assert_has_calls([call(), call(pretty=True)])
        mock_id.assert_has_calls([call(), call(), call()])
        mock_like.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockeduser")
    @patch("src.app.screens.greetings_screen.distro.id", return_value="debian")
    @patch("src.app.screens.greetings_screen.distro.like", return_value="debian")
    @patch("src.app.screens.greetings_screen.distro.name", return_value="mockos")
    def test_render_main_screen_update_check_user_in_debian(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="GreetingsScreen", key="check_user")
        message = "[size=32sp][color=#efcc00]Setup mockeduser for mockos[/color][/size]"

        # default assertions
        self.assertEqual(button.text, message)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_environ_get.assert_called_once_with("USER")
        mock_name.assert_called_once()
        mock_id.assert_called_once()
        assert not mock_like.called

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockeduser")
    @patch("src.app.screens.greetings_screen.distro.id", return_value="mockos")
    @patch("src.app.screens.greetings_screen.distro.like", return_value="debian")
    @patch("src.app.screens.greetings_screen.distro.name", return_value="mockos")
    def test_render_main_screen_update_check_user_in_debian_like(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="GreetingsScreen", key="check_user")
        message = "[size=32sp][color=#efcc00]Setup mockeduser for mockos[/color][/size]"

        # default assertions
        self.assertEqual(button.text, message)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_environ_get.assert_called_once_with("USER")
        mock_name.assert_called_once()
        mock_id.assert_called_once()
        mock_like.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockeduser")
    @patch("src.app.screens.greetings_screen.distro.id", return_value="arch")
    @patch("src.app.screens.greetings_screen.distro.like", return_value="arch")
    @patch("src.app.screens.greetings_screen.distro.name", return_value="mockos")
    def test_render_main_screen_update_check_user_in_arch(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="GreetingsScreen", key="check_user")
        message = "[size=32sp][color=#efcc00]Setup mockeduser for mockos[/color][/size]"

        # default assertions
        self.assertEqual(button.text, message)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_environ_get.assert_called_once_with("USER")
        mock_name.assert_called_once()
        mock_id.assert_has_calls([call(), call()])
        mock_like.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockeduser")
    @patch("src.app.screens.greetings_screen.distro.id", return_value="manjaro")
    @patch("src.app.screens.greetings_screen.distro.like", return_value="arch")
    @patch("src.app.screens.greetings_screen.distro.name", return_value="mockos")
    def test_render_main_screen_update_check_user_in_manjaro(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = GreetingsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="GreetingsScreen", key="check_user")
        message = "[size=32sp][color=#efcc00]Setup mockeduser for mockos[/color][/size]"

        # default assertions
        self.assertEqual(button.text, message)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_environ_get.assert_called_once_with("USER")
        mock_name.assert_called_once()
        mock_id.assert_has_calls([call(), call(), call()])
        mock_like.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "mockos")
    @patch("src.app.screens.greetings_screen.App.get_running_app")
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
    @patch("src.app.screens.greetings_screen.App.get_running_app")
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
        mock_partial.assert_called_with(
            screen.update, name=screen.name, key="check_user"
        )
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "macos")
    @patch("src.app.screens.greetings_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.partial")
    def test_on_enter_in_macos(self, mock_partial, mock_get_running_app):
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
        mock_partial.assert_called_with(
            screen.update, name=screen.name, key="skip_permission_message"
        )
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "win32")
    @patch("src.app.screens.greetings_screen.App.get_running_app")
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
        mock_partial.assert_called_with(
            screen.update, name=screen.name, key="skip_permission_message"
        )
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.greetings_screen.App.get_running_app")
    def test_render_button(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        #
        self.assertEqual(len(buttons), 1)
        self.assertEqual(buttons[0].id, "greetings_screen_button")

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.greetings_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_background")
    def test_on_pressed_greetings_button(
        self, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]
        action = getattr(screen, "on_press_greetings_screen_button")

        # Do the test
        action(button)

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid="greetings_screen_button", rgba=(0.25, 0.25, 0.25, 1)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.greetings_screen.App.get_running_app")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_background")
    @patch("src.app.screens.greetings_screen.SudoerLinux.exec")
    def test_on_release_greetings_button(
        self, mock_exec, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = GreetingsScreen()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        screen.user = "mockeduser"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]
        action = getattr(screen, "on_release_greetings_screen_button")

        # Do the test
        action(button)

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid="greetings_screen_button", rgba=(0, 0, 0, 1)
        )
        mock_exec.assert_called_once()

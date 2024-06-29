import sys
from unittest.mock import patch, MagicMock, call
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.check_permissions_screen import CheckPermissionsScreen


# WARNING: Do not run these tests on windows
# they will break because it do not have the builtin 'grp' module
@mark.skipif(sys.platform == "win32", reason="does not run on windows")
class TestAboutScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_fail_invalid_name(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = CheckPermissionsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="Mock")

        self.assertEqual(str(exc_info.exception), "Invalid screen: Mock")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_fail_invalid_key(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = CheckPermissionsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="ConfigKruxInstaller", key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid key: 'mock'")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.os.environ.get",
        return_value="mockeduser",
    )
    @patch("src.app.screens.check_permissions_screen.distro.id", return_value="mockos")
    @patch(
        "src.app.screens.check_permissions_screen.distro.like", return_value="mockos"
    )
    @patch(
        "src.app.screens.check_permissions_screen.distro.name", return_value="mockos"
    )
    def test_update_fail_check_user(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        with self.assertRaises(RuntimeError) as exc_info:
            screen.update(name="CheckPermissionsScreen", key="check_user")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Not implemented for 'mockos'")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_environ_get.assert_called_once_with("USER")
        mock_name.assert_has_calls([call(), call(pretty=True)])
        mock_id.assert_has_calls([call(), call()])
        mock_like.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.os.environ.get",
        return_value="mockeduser",
    )
    @patch("src.app.screens.check_permissions_screen.distro.id", return_value="debian")
    @patch(
        "src.app.screens.check_permissions_screen.distro.like", return_value="debian"
    )
    @patch(
        "src.app.screens.check_permissions_screen.distro.name", return_value="mockos"
    )
    def test_update_check_user_in_debian(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="check_user")
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.os.environ.get",
        return_value="mockeduser",
    )
    @patch("src.app.screens.check_permissions_screen.distro.id", return_value="mockos")
    @patch(
        "src.app.screens.check_permissions_screen.distro.like", return_value="debian"
    )
    @patch(
        "src.app.screens.check_permissions_screen.distro.name", return_value="mockos"
    )
    def test_update_check_user_in_debian_like(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="check_user")
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.os.environ.get",
        return_value="mockeduser",
    )
    @patch("src.app.screens.check_permissions_screen.distro.id", return_value="arch")
    @patch("src.app.screens.check_permissions_screen.distro.like", return_value="arch")
    @patch(
        "src.app.screens.check_permissions_screen.distro.name", return_value="mockos"
    )
    def test_check_user_in_arch(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="check_user")
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.distro.name", return_value="MockOS"
    )
    @patch("src.app.screens.check_permissions_screen.grp")
    def test_check_group_not_in_group(
        self, mock_grp, mock_distro_name, mock_get_running_app
    ):

        mocked_group = MagicMock()
        mocked_group.gr_name = "mockedgroup"
        mocked_group.__iter__ = MagicMock(return_value=iter([0, 1, 2, 3]))

        attrs = {
            "getgrall.return_value": [mocked_group],
        }
        mock_grp.configure_mock(**attrs)

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="check_group")

        # default assertions
        # self.assertEqual(button.text, message)
        self.assertEqual(screen.in_dialout, False)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_distro_name.assert_called_once_with(pretty=True)
        mock_grp.getgrall.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.os.environ.get",
        return_value="mockeduser",
    )
    @patch("src.app.screens.check_permissions_screen.distro.id", return_value="manjaro")
    @patch("src.app.screens.check_permissions_screen.distro.like", return_value="arch")
    @patch(
        "src.app.screens.check_permissions_screen.distro.name", return_value="mockos"
    )
    def test_update_check_user_in_manjaro(
        self, mock_name, mock_like, mock_id, mock_environ_get, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="check_user")
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_make_on_permission_created(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
        screen.user = "mockeduser"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="make_on_permission_created")
        text = "\n".join(
            [
                "[size=32sp][color=#efcc00]mocked command[/color][/size]",
                "",
                "[size=16sp]You may need to logout (or even reboot)",
                "and back in for the new group to take effect.",
                "",
                "Do not worry, this message won't appear again.[/size]",
            ]
        )
        screen.on_permission_created(output="mocked command")

        # default assertions
        self.assertFalse(screen.on_permission_created is None)
        self.assertEqual(button.text, text)
        self.assertEqual(screen.bin, None)
        self.assertEqual(screen.bin_args, None)
        self.assertEqual(screen.group, None)
        self.assertEqual(screen.user, None)

        # Do test again
        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "mockos")
    @patch("src.app.screens.check_permissions_screen.App.get_running_app")
    @patch("src.app.screens.check_permissions_screen.partial")
    def test_on_enter(self, mock_partial, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock()

        screen = CheckPermissionsScreen()
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
        mock_partial.assert_called_once_with(
            screen.update, name="CheckPermissionsScreen", key="check_user"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.check_permissions_screen.App.get_running_app")
    def test_render_button(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = CheckPermissionsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        #
        self.assertEqual(len(buttons), 1)
        self.assertEqual(buttons[0].id, "check_permissions_screen_button")

        # patch assertions
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.check_permissions_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.CheckPermissionsScreen.set_background"
    )
    def test_on_pressed_greetings_button(
        self, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = CheckPermissionsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]
        action = getattr(screen, "on_press_check_permissions_screen_button")

        # Do the test
        action(button)

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid="check_permissions_screen_button", rgba=(0.25, 0.25, 0.25, 1)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.check_permissions_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.CheckPermissionsScreen.set_background"
    )
    @patch("src.app.screens.check_permissions_screen.SudoerLinux.exec")
    def test_fail_on_release_greetings_button(
        self, mock_exec, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = CheckPermissionsScreen()
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
        action = getattr(screen, "on_release_check_permissions_screen_button")

        # Do the test
        with self.assertRaises(RuntimeError) as exc_info:
            action(button)

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid on_permission_created: None")

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid="check_permissions_screen_button", rgba=(0, 0, 0, 1)
        )
        assert not mock_exec.called

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.screens.check_permissions_screen.App.get_running_app")
    @patch(
        "src.app.screens.check_permissions_screen.CheckPermissionsScreen.set_background"
    )
    @patch("src.app.screens.check_permissions_screen.SudoerLinux.exec")
    def test_on_release_greetings_button(
        self, mock_exec, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = CheckPermissionsScreen()
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
        action = getattr(screen, "on_release_check_permissions_screen_button")

        # Do the test
        screen.update(name="CheckPermissionsScreen", key="make_on_permission_created")
        action(button)

        # patch assertions
        mock_get_running_app.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid="check_permissions_screen_button", rgba=(0, 0, 0, 1)
        )
        mock_exec.assert_called_once()

import os
import sys
from pathlib import Path
import builtins
from unittest.mock import MagicMock, patch, mock_open
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from src.app.screens.greetings_screen import GreetingsScreen


class TestAboutScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        # Unschedule all pending Clock events to prevent race conditions
        # with subsequent tests
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        image = grid.children[0]

        # default assertions
        root = Path(__file__).parent.parent
        asset = os.path.join(root, "assets", "logo.png")
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "GreetingsScreen")
        self.assertEqual(screen.id, "greetings_screen")
        self.assertEqual(image.source, asset)
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_on_enter(self, mock_schedule_once, mock_partial, mock_get_locale):
        screen = GreetingsScreen()
        self.render(screen)
        screen.on_enter()

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_get_locale.assert_called()
        mock_partial.assert_called()
        mock_schedule_once.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.check_dialout_permission")
    def test_update_check_permission_screen(
        self, mock_check_permission, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-permission")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_check_permission.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.check_internet_connection")
    def test_update_check_internet_connection(
        self, mock_check_internet, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-internet-connection")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_check_internet.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID_LIKE=debian",
    )
    def test_get_os_dialout_group_debian(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "debian")
        self.assertEqual(group[1], "dialout")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID_LIKE=rhel",
    )
    def test_get_os_dialout_group_rhel(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "rhel")
        self.assertEqual(group[1], "dialout")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID_LIKE=suse",
    )
    def test_get_os_dialout_group_suse(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "suse")
        self.assertEqual(group[1], "dialout")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=arch",
    )
    def test_get_os_dialout_group_arch(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "arch")
        self.assertEqual(group[1], "uucp")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=manjaro",
    )
    def test_get_os_dialout_group_manjaro(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "manjaro")
        self.assertEqual(group[1], "uucp")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=slackware",
    )
    def test_get_os_dialout_group_slackware(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "slackware")
        self.assertEqual(group[1], "uucp")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=gentoo",
    )
    def test_get_os_dialout_group_gentoo(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "gentoo")
        self.assertEqual(group[1], "uucp")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=alpine",
    )
    def test_get_os_dialout_group_alpine(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "alpine")
        self.assertEqual(group[1], "dialout")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=clear-linux",
    )
    def test_get_os_dialout_group_clear_linux(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "clear-linux")
        self.assertEqual(group[1], "dialout")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=solus",
    )
    def test_get_os_dialout_group_solus(self, open_mock, mock_get_locale):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], "solus")
        self.assertEqual(group[1], "dialout")

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data="ID=mockos\nPRETTY_NAME=MockOS",
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_get_os_dialout_group_not_supported(
        self, mock_redirect_exception, open_mock, mock_get_locale
    ):
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], None)

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")
        mock_redirect_exception.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_get_os_dialout_group_file_not_found(
        self, mock_redirect_exception, open_mock, mock_get_locale
    ):
        open_mock.side_effect = FileNotFoundError()
        screen = GreetingsScreen()
        group = screen.get_os_dialout_group()
        self.assertEqual(group[0], None)

        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")
        mock_redirect_exception.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch("sys.platform", "linux")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_is_user_not_in_dialout(self, mock_get_locale):
        # Create a mock grp module
        mock_grp = MagicMock()
        mock_grp.getgrall.return_value = [
            MagicMock(gr_name="dialout", gr_passwd="x", gr_gid=1234, gr_mem=["brltty"])
        ]

        # Initialize the screen FIRST
        screen = GreetingsScreen()

        # Then patch when calling the method
        with patch.dict("sys.modules", {"grp": mock_grp}):
            is_in_dialout = screen.is_user_in_dialout_group(
                user="mockuser", group="dialout"
            )

            # Assertions
            self.assertEqual(is_in_dialout, False)
            mock_get_locale.assert_called()
            mock_grp.getgrall.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch("sys.platform", "linux")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_is_user_in_dialout(self, mock_get_locale):
        # Create a mock grp module
        mock_grp = MagicMock()
        mock_grp.getgrall.return_value = [
            MagicMock(
                gr_name="dialout",
                gr_passwd="x",
                gr_gid=1234,
                gr_mem=["brltty", "mockuser"],
            )
        ]

        # Initialize the screen FIRST
        screen = GreetingsScreen()

        # Then patch when calling the method
        with patch.dict("sys.modules", {"grp": mock_grp}):
            is_in_dialout = screen.is_user_in_dialout_group(
                user="mockuser", group="dialout"
            )

            self.assertEqual(is_in_dialout, True)
            mock_get_locale.assert_called()
            mock_grp.getgrall.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.manager")
    @patch("src.app.screens.greetings_screen.Selector")
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_screen")
    def test_check_internet_connection(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_selector,
        mock_manager,
        mock_get_locale,
    ):
        mock_manager.get_screen = MagicMock()
        mock_manager.get_screen.update = MagicMock()
        mock_selector.return_value = MagicMock(releases=["v0.0.1"])
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-internet-connection")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_manager.get_screen.assert_called_once()
        mock_partial.assert_called_once_with(
            mock_manager.get_screen().update,
            name="GreetingsScreen",
            key="version",
            value="v0.0.1",
        )
        mock_schedule_once.assert_called()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.Selector", side_effect=[Exception("Mocked")]
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.redirect_exception")
    def test_fail_check_internet_connection(
        self, mock_redirect_exception, mock_selector, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-internet-connection")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_selector.assert_called()
        mock_redirect_exception.assert_called()

    @patch("sys.platform", "win32")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_pass_check_dialout_permission_not_linux(
        self, mock_schedule_once, mock_partial, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-permission")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_partial.assert_called_once_with(
            screen.update, name="GreetingsScreen", key="check-internet-connection"
        )
        mock_schedule_once.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows or darwin",
    )
    @patch("sys.platform", "linux")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockuser")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.GreetingsScreen.get_os_dialout_group",
        return_value=["debian", "dialout"],
    )
    @patch(
        "src.app.screens.greetings_screen.GreetingsScreen.is_user_in_dialout_group",
        return_value=False,
    )
    @patch("src.app.screens.base_screen.BaseScreen.manager")
    def test_check_dialout_permission_not_in_dialout(
        self,
        mock_manager,
        mock_in_dialout,
        mock_get_os,
        mock_get_locale,
        mock_environ_get,
    ):
        mock_manager.get_screen = MagicMock()
        mock_manager.get_screen.update = MagicMock()
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.check_dialout_permission()

        # patch assertions
        mock_environ_get.assert_called()
        mock_get_locale.assert_called()
        mock_get_os.assert_called()
        mock_in_dialout.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows or darwin",
    )
    @patch("sys.platform", "linux")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockuser")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.GreetingsScreen.get_os_dialout_group",
        return_value=["debian", "dialout"],
    )
    @patch(
        "src.app.screens.greetings_screen.GreetingsScreen.is_user_in_dialout_group",
        return_value=True,
    )
    @patch("src.app.screens.base_screen.BaseScreen.manager")
    def test_check_dialout_permission_in_dialout(
        self,
        mock_manager,
        mock_in_dialout,
        mock_get_os,
        mock_get_locale,
        mock_environ_get,
    ):
        mock_manager.get_screen = MagicMock()
        mock_manager.get_screen.update = MagicMock()
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.check_dialout_permission()

        # patch assertions
        mock_environ_get.assert_called()
        mock_get_locale.assert_called()
        mock_get_os.assert_called()
        mock_in_dialout.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.greetings_screen.open",
        new_callable=mock_open,
        read_data='ID="nixos"\nVERSION_ID="25.11"\nPRETTY_NAME="NixOS 25.11"\n',
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale",
        return_value="en_US.UTF-8",
    )
    def test_get_os_dialout_group_nixos(self, mock_get_locale, open_mock):
        screen = GreetingsScreen()
        distro, group = screen.get_os_dialout_group()

        self.assertEqual(distro, "nixos")
        self.assertEqual(group, "dialout")
        mock_get_locale.assert_called()
        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_is_user_in_dialout_when_grp_import_fails(self, mock_get_locale):
        """Test that is_user_in_dialout_group returns False when grp import raises ImportError"""
        screen = GreetingsScreen()

        # Create a custom import function that raises ImportError for grp
        original_import = builtins.__import__

        def custom_import(name, *args, **kwargs):
            if name == "grp":
                raise ImportError("No module named 'grp'")
            return original_import(name, *args, **kwargs)

        # Patch __import__ to use our custom function
        with patch("builtins.__import__", side_effect=custom_import):
            is_in_dialout = screen.is_user_in_dialout_group(
                user="mockuser", group="dialout"
            )

            # Assertions
            self.assertEqual(is_in_dialout, False)
            mock_get_locale.assert_called()

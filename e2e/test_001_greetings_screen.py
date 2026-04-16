import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from pytest import mark

from src.app.screens.greetings_screen import GreetingsScreen


class TestAboutScreen(GraphicUnitTest):
    @classmethod
    def teardown_class(cls):
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

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        image = grid.children[0]

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

        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-permission")

        mock_get_locale.assert_called_once()
        mock_check_permission.assert_called_once()

    @patch("sys.platform", "win32")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_screen")
    def test_pass_check_dialout_permission_not_linux(
        self, mock_set_screen, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        EventLoop.ensure_window()

        screen.check_dialout_permission()

        mock_get_locale.assert_called_once()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="left")

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
        read_data="ID=mockos\nPRETTY_NAME=MockOS",
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.redirect_exception")
    def test_get_os_dialout_group_unsupported(
        self, mock_redirect_exception, _open_mock, mock_get_locale
    ):
        screen = GreetingsScreen()
        screen.get_os_dialout_group()

        mock_get_locale.assert_called()
        mock_redirect_exception.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.open",
        side_effect=FileNotFoundError,
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.redirect_exception")
    def test_get_os_dialout_group_file_not_found(
        self, mock_redirect_exception, _open_mock, mock_get_locale
    ):
        screen = GreetingsScreen()
        screen.get_os_dialout_group()

        mock_get_locale.assert_called()
        mock_redirect_exception.assert_called_once()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
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

        EventLoop.ensure_window()

        screen.check_dialout_permission()

        mock_environ_get.assert_called()
        mock_get_locale.assert_called()
        mock_get_os.assert_called()
        mock_in_dialout.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
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

        EventLoop.ensure_window()

        screen.check_dialout_permission()

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
        screen = GreetingsScreen()

        if isinstance(__builtins__, dict):
            original_import = __builtins__["__import__"]
        else:
            original_import = __builtins__.__import__

        def custom_import(name, *args, **kwargs):
            if name == "grp":
                raise ImportError("No module named 'grp'")
            return original_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=custom_import):
            is_in_dialout = screen.is_user_in_dialout_group(
                user="mockuser", group="dialout"
            )

            self.assertEqual(is_in_dialout, False)
            mock_get_locale.assert_called()

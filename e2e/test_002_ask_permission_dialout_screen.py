import os
import sys
from unittest.mock import patch, MagicMock
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.ask_permission_dialout_screen import AskPermissionDialoutScreen


# WARNING: Do not run these tests on windows
# they will break because it do not have the builtin 'grp' module
@mark.skipif(sys.platform == "win32", reason="does not run on windows or macos")
class TestAskPermissionDialoutScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        noto_sans_path = os.path.join(assets_path, "NotoSansCJK_Cy_SC_KR_Krux.ttf")
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_label(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        self.assertTrue("ask_permission_dialout_screen_label" in screen.ids)

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_update_user(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="user", value="mockeduser")
        self.assertEqual(screen.user, "mockeduser")

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_update_distro(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="distro", value="mockos")
        self.assertEqual(screen.distro, "mockos")

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.ask_permission_dialout_screen.AskPermissionDialoutScreen.show_warning"
    )
    def test_on_update_screen(self, mock_show_warning, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="screen")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_show_warning.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_update_group(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="group", value="mockedgroup")
        self.assertEqual(screen.group, "mockedgroup")

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_show_warning(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.user = "user"
        screen.group = "group"
        screen.distro = "mockos"
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        text = "".join(
            [
                "[color=#efcc00]WARNING[/color]",
                "\n",
                'This is the first run of KruxInstaller in "mockos"',
                "\n",
                "and it appears that you do not have privileged access to make flash procedures.",
                "\n",
                "To proceed, click in the Allow button and a prompt will ask for your password",
                "\n",
                "to execute the following command:",
                "\n",
                "[color=#00ff00]",
                "/usr/bin/usermod -a -G group user",
                "[/color]",
                "\n",
                "\n",
                "[color=#00FF00][ref=Allow]Allow[/ref][/color]",
                "        ",
                "[color=#FF0000][ref=Deny]Deny[/ref][/color]",
            ]
        )

        screen.show_warning()
        self.assertEqual(screen.ids[f"{screen.id}_label"].text, text)

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.ask_permission_dialout_screen.SudoerLinux.exec")
    def test_press_allow(self, mock_exec, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        screen.user = "mockeduser"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        action = getattr(screen, f"on_ref_press_{screen.id}_label")
        action("Allow")

        # patch assertions
        on_permission_created = getattr(
            AskPermissionDialoutScreen, "on_permission_created"
        )
        mock_get_locale.assert_called_once()
        mock_exec.assert_called_once_with(
            cmd=["/usr/bin/usermod", "-a", "-G", "mockedgroup", "mockeduser"],
            env={},
            callback=on_permission_created,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.ask_permission_dialout_screen.SudoerLinux.exec")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_press_allow(
        self, mock_redirect_exception, mock_exec, mock_get_locale
    ):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        screen.user = "mockeduser"

        mock_exec.side_effect = RuntimeError("Mocked error")

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]
        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(button, "Allow")

        # patch assertions
        on_permission_created = getattr(
            AskPermissionDialoutScreen, "on_permission_created"
        )
        mock_get_locale.assert_called_once()
        mock_exec.assert_called_once_with(
            cmd=["/usr/bin/usermod", "-a", "-G", "mockedgroup", "mockeduser"],
            env={},
            callback=on_permission_created,
        )
        mock_redirect_exception.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.quit_app")
    def test_press_deny(self, mock_quit_app, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        screen.user = "mockeduser"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]
        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(button, "Deny")

        mock_get_locale.assert_called_once()
        mock_quit_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_permission_created(self, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.bin = "mock"
        screen.bin_args = ["-a", "-G"]
        screen.group = "mockedgroup"
        screen.user = "mockeduser"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        action = getattr(AskPermissionDialoutScreen, "on_permission_created")
        action("ok")

        text = "".join(
            [
                "You may need to logout (or even reboot)",
                "\n",
                "and back in for the new group to take effect.",
                "\n",
                "\n",
                "Do not worry, this message won't appear again.",
            ]
        )

        self.assertEqual(screen.ids[f"{screen.id}_label"].text, text)

        # patch assertions
        mock_get_locale.assert_called_once()

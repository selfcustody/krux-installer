import os
import sys
from unittest.mock import patch, MagicMock, call
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.ask_permission_dialout_screen import AskPermissionDialoutScreen


# WARNING: Do not run these tests on windows
# they will break because it do not have the builtin 'grp' module
@mark.skipif(sys.platform == "win32", reason="does not run on windows")
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
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_update_fail_invalid_name(self, mock_redirect_error, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name="MockScreen")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_redirect_error.assert_called_once_with(msg="Invalid screen: 'MockScreen'")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_update_fail_invalid_key(self, mock_redirect_error, mock_get_locale):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="ConfigKruxInstaller", key="mock")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_redirect_error.assert_called_once_with(msg="Invalid key: 'mock'")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_update_fail_locale(
        self,
        mock_redirect_error,
        mock_get_locale,
    ):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="AskPermissionDialoutScreen", key="locale")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_redirect_error.assert_called_once_with(
            msg="Invalid value for key 'locale': 'None'"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_update_fail_user(
        self,
        mock_redirect_error,
        mock_get_locale,
    ):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="AskPermissionDialoutScreen", key="user")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_redirect_error.assert_called_once_with(
            msg="Invalid value for key 'user': 'None'"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_update_fail_group(
        self,
        mock_redirect_error,
        mock_get_locale,
    ):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="AskPermissionDialoutScreen", key="group")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_redirect_error.assert_called_once_with(
            msg="Invalid value for key 'group': 'None'"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_update_fail_distro(
        self,
        mock_redirect_error,
        mock_get_locale,
    ):
        screen = AskPermissionDialoutScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="AskPermissionDialoutScreen", key="distro")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_redirect_error.assert_called_once_with(
            msg="Invalid value for key 'distro': 'None'"
        )

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

        screen.update(name="AskPermissionDialoutScreen", key="user", value="mockeduser")
        screen.update(name="AskPermissionDialoutScreen", key="group", value="dialout")
        screen.update(name="AskPermissionDialoutScreen", key="distro", value="mockos")
        screen.update(name="AskPermissionDialoutScreen", key="screen")
        self.assertTrue("ask_permission_dialout_screen_label" in screen.ids)

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
        mock_get_locale.assert_called_once()
        mock_exec.assert_called_once_with(
            cmd=["/usr/bin/usermod", "-a", "-G", "mockedgroup", "mockeduser"],
            env={},
            callback=screen.on_permission_created,
        )

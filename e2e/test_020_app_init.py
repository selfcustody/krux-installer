import os
import sys
from unittest.mock import patch, mock_open, MagicMock
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from kivy.uix.screenmanager import ScreenManager
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app import KruxInstallerApp


class TestConfigKruxInstaller(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        font_name = "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
        noto_sans_path = os.path.join(assets_path, font_name)
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @classmethod
    def teardown_class(cls):
        # Unschedule all pending Clock events to prevent race conditions
        # with subsequent tests
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LANG": "en_US.UTF-8"}, clear=True)
    def test_init(self):
        app = KruxInstallerApp()
        self.assertEqual(len(app.screens), 0)
        self.assertIsInstance(app.screen_manager, ScreenManager)

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("builtins.open", new_callable=mock_open, read_data="ID_LIKE=debian")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_debian(self, mock_get_destdir_assets, mock_get_locale, open_mock):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("builtins.open", new_callable=mock_open, read_data="ID_LIKE=rhel")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_rhel(self, mock_get_destdir_assets, mock_get_locale, open_mock):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("builtins.open", new_callable=mock_open, read_data="ID_LIKE=suse")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_suse(self, mock_get_destdir_assets, mock_get_locale, open_mock):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called_once_with("/etc/os-release", mode="r", encoding="utf-8")
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("builtins.open", new_callable=mock_open, read_data="ID=arch")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_arch(self, mock_get_destdir_assets, mock_get_locale, open_mock):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called()
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("builtins.open", new_callable=mock_open, read_data="ID=alpine")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_alpine(self, mock_get_destdir_assets, mock_get_locale, open_mock):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called()
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="ID=mockos\nPRETTY_NAME=MockOS",
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_build_unrecognized(
        self,
        mock_redirect_exception,
        mock_get_destdir_assets,
        mock_get_locale,
        open_mock,
    ):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called()
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()
        mock_redirect_exception.assert_called()

    @mark.skipif(
        sys.platform in ("win32"),
        reason="does not run on windows",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("builtins.open", new_callable=mock_open)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_build_linux_filenotfound(
        self,
        mock_redirect_exception,
        mock_get_destdir_assets,
        mock_get_locale,
        open_mock,
    ):
        open_mock.return_value.__enter__.side_effect = [FileNotFoundError, MagicMock()]
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "AskPermissionDialoutScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        open_mock.assert_called()
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()
        mock_redirect_exception.assert_called()

    @patch("sys.platform", "win32")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_win32(self, mock_get_destdir_assets, mock_get_locale):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

    @patch("sys.platform", "darwin")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_darwin(self, mock_get_destdir_assets, mock_get_locale):
        app = KruxInstallerApp()
        app.build()

        screens = (
            "GreetingsScreen",
            "MainScreen",
            "SelectDeviceScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "AboutScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningAlreadyDownloadedScreen",
            "WarningWipeScreen",
            "FlashScreen",
            "WipeScreen",
            "ErrorScreen",
        )
        for screen in screens:
            self.assertFalse(app.screen_manager.get_screen(screen) is None)

        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

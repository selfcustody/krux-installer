import os
from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
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
        noto_sans_path = os.path.join(assets_path, "NotoSansCJK_Cy_SC_KR_Krux.ttf")
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LANG": "en_US.UTF-8"}, clear=True)
    def test_init(self):
        app = KruxInstallerApp()
        self.assertEqual(len(app.screens), 0)
        self.assertIsInstance(app.screen_manager, ScreenManager)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_linux(self, mock_get_destdir_assets, mock_get_locale):
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

        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()

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

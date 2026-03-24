import os
from unittest.mock import patch
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app import KruxInstallerApp, SCREEN_PARENTS

# pylint: disable=unused-argument,protected-access


class TestAppKeyNavigation(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        font_name = "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
        noto_sans_path = os.path.join(assets_path, font_name)
        LabelBase.register(DEFAULT_FONT, noto_sans_path)
        cls._patch_bind = patch(
            "kivy.core.window.Window.bind", new=lambda *a, **k: None
        )
        cls._patch_bind.start()

    @classmethod
    def tearDownClass(cls):
        for event in Clock.get_events():
            Clock.unschedule(event)
        if getattr(cls, "_patch_bind", None):
            try:
                cls._patch_bind.stop()
            except RuntimeError:
                pass
        EventLoop.exit()

    def test_screen_parents_has_greetings_as_root(self):
        self.assertIsNone(SCREEN_PARENTS["GreetingsScreen"])

    def test_screen_parents_flash_screen_starts_as_none(self):
        self.assertIsNone(SCREEN_PARENTS["FlashScreen"])

    def test_screen_parents_main_screen_points_to_greetings(self):
        self.assertEqual(SCREEN_PARENTS["MainScreen"], "GreetingsScreen")

    def test_screen_parents_error_screen_points_to_greetings(self):
        self.assertEqual(SCREEN_PARENTS["ErrorScreen"], "GreetingsScreen")

    def test_screen_parents_all_expected_screens_present(self):
        expected = {
            "GreetingsScreen",
            "MainScreen",
            "SelectVersionScreen",
            "SelectOldVersionScreen",
            "WarningBetaScreen",
            "SelectDeviceScreen",
            "AboutScreen",
            "WarningAlreadyDownloadedScreen",
            "DownloadStableZipScreen",
            "DownloadStableZipSha256Screen",
            "DownloadStableZipSigScreen",
            "DownloadSelfcustodyPemScreen",
            "VerifyStableZipScreen",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "WarningWipeScreen",
            "WipeScreen",
            "WarningBeforeAirgapUpdateScreen",
            "AirgapUpdateScreen",
            "WarningAfterAirgapUpdateScreen",
            "FlashScreen",
            "ErrorScreen",
        }
        for screen in expected:
            self.assertIn(screen, SCREEN_PARENTS)

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_instance_screen_parents_is_copy_of_module_map(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        self.assertEqual(app.screen_parents, SCREEN_PARENTS)
        # mutating instance does not affect module-level map
        app.screen_parents["FlashScreen"] = "UnzipStableScreen"
        self.assertIsNone(SCREEN_PARENTS["FlashScreen"])

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_non_esc_returns_false(self, mock_destdir, mock_get_locale):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "MainScreen"

        result = app._on_key_down(None, 97, None)  # 'a' key

        self.assertFalse(result)
        self.assertEqual(app.screen_manager.current, "MainScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_main_goes_to_greetings(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "MainScreen"

        with patch.object(app, "_reset_main_screen") as mock_reset:
            result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "GreetingsScreen")
        self.assertEqual(app.screen_manager.transition.direction, "right")
        mock_reset.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_select_version_goes_to_main(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "SelectVersionScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "MainScreen")
        self.assertEqual(app.screen_manager.transition.direction, "right")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_select_old_version_goes_to_select_version(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "SelectOldVersionScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "SelectVersionScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_warning_beta_goes_to_select_version(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "WarningBetaScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "SelectVersionScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_select_device_goes_to_main(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "SelectDeviceScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "MainScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_about_goes_to_main(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "AboutScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "MainScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_error_screen_goes_to_greetings(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "ErrorScreen"

        with patch.object(app, "_reset_main_screen") as mock_reset:
            result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "GreetingsScreen")
        mock_reset.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_wipe_goes_to_warning_wipe(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "WipeScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "WarningWipeScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_from_airgap_goes_to_warning_before_airgap(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "AirgapUpdateScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "WarningBeforeAirgapUpdateScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_on_greetings_stops_app(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_manager.current = "GreetingsScreen"

        with patch.object(app, "stop") as mock_stop:
            result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        mock_stop.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_on_flash_screen_no_parent_stops_app(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_parents["FlashScreen"] = None
        app.screen_manager.current = "FlashScreen"

        with patch.object(app, "stop") as mock_stop:
            result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        mock_stop.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_on_flash_screen_stable_path(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_parents["FlashScreen"] = "UnzipStableScreen"
        app.screen_manager.current = "FlashScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "UnzipStableScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_on_flash_screen_beta_path(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()
        app.screen_parents["FlashScreen"] = "DownloadBetaScreen"
        app.screen_manager.current = "FlashScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(app.screen_manager.current, "DownloadBetaScreen")

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_reset_main_screen_schedules_device_reset(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        app.build()

        with patch("kivy.clock.Clock.schedule_once") as mock_schedule:
            app._reset_main_screen()
            mock_schedule.assert_called_once()

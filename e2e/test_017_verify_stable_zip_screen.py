import sys
from unittest.mock import patch, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.verify_stable_zip_screen import (
    VerifyStableZipScreen,
)


class TestVerifyStableZipScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(grid.id, f"{screen.id}_grid")
        self.assertFalse(screen.success)
        self.assertTrue(
            hasattr(VerifyStableZipScreen, "on_ref_press_verify_stable_zip_screen")
        )

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.verify_stable_zip_screen.Sha256Verifyer")
    @patch("src.app.screens.verify_stable_zip_screen.Sha256CheckVerifyer")
    def test_verify_sha256(self, mock_check_verifyer, mock_verifyer, mock_get_locale):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.verify_sha256(assets_dir="mockdir", version="v0.0.1")

        # patch assertions
        mock_get_locale.assert_called()
        mock_verifyer.assert_called_once_with(filename="mockdir/krux-v0.0.1.zip")
        mock_check_verifyer.assert_called_once_with(
            filename="mockdir/krux-v0.0.1.zip.sha256.txt"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.verify_stable_zip_screen.SigVerifyer")
    @patch("src.app.screens.verify_stable_zip_screen.PemCheckVerifyer")
    @patch("src.app.screens.verify_stable_zip_screen.SigCheckVerifyer")
    def test_verify_signature(
        self,
        mock_sig_check_verifyer,
        mock_pem_check_verifyer,
        mock_sig_verifyer,
        mock_get_locale,
    ):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.verify_signature(assets_dir="mockdir", version="v0.0.1")

        # patch assertions
        mock_get_locale.assert_called()
        mock_sig_check_verifyer.assert_called_once_with(
            filename="mockdir/krux-v0.0.1.zip.sig"
        )
        mock_pem_check_verifyer.assert_called_once_with(
            filename="mockdir/selfcustody.pem"
        )
        mock_sig_verifyer.assert_called_once_with(
            filename="mockdir/krux-v0.0.1.zip",
            regexp=r"^.*\.zip$",
            signature=mock_sig_check_verifyer().data,
            pubkey=mock_pem_check_verifyer().data,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_pre_enter(self, mock_get_locale):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        fontsize_mm = 0

        if sys.platform in ("linux", "win32"):
            fontsize_mm = window.size[0] // 24

        if sys.platform == "darwin":
            fontsize_mm = window.size[0] // 48

        screen.on_pre_enter()

        text = "".join(
            [
                f"[size={fontsize_mm}sp]",
                "[color=#efcc00]",
                "Verifying integrity and authenticity",
                "[/color]",
                "[/size]",
            ]
        )
        self.assertEqual(len(screen.ids["verify_stable_zip_screen_grid"].children), 1)
        self.assertEqual(screen.ids["verify_stable_zip_screen_label"].text, text)

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_fail_update_invalid_name(self, mock_redirect_error, mock_get_locale):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="MockScreen")

        # patch assertions
        mock_get_locale.assert_called()
        mock_redirect_error.assert_called_once_with("Invalid screen name: MockScreen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = VerifyStableZipScreen()
        old_loc = screen.locale
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="pt_BR.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "pt_BR.UTF-8")
        self.assertFalse(screen.locale == old_loc)

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.manager")
    @patch("src.app.screens.verify_stable_zip_screen.partial")
    @patch("src.app.screens.verify_stable_zip_screen.Clock.schedule_once")
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.set_screen")
    def test_on_press_proceed(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_manager,
        mock_get_locale,
    ):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # DO tests
        screen.on_pre_enter()
        action = getattr(VerifyStableZipScreen, f"on_ref_press_{screen.id}")
        action("Mock", "UnzipStableScreen")

        # patch assertions
        mock_get_locale.assert_called()
        mock_manager.get_screen.assert_has_calls(
            [call("MainScreen"), call("UnzipStableScreen")]
        )
        mock_partial.assert_has_calls(
            [
                call(
                    mock_manager.get_screen().update,
                    name="VerifyStableZipScreen",
                    key="version",
                    value=mock_manager.get_screen().version,
                ),
                call(
                    mock_manager.get_screen().update,
                    name="VerifyStableZipScreen",
                    key="device",
                    value=mock_manager.get_screen().device,
                ),
                call(
                    mock_manager.get_screen().update,
                    name="VerifyStableZipScreen",
                    key="clear",
                ),
                call(
                    mock_manager.get_screen().update,
                    name="VerifyStableZipScreen",
                    key="flash-button",
                ),
                call(
                    mock_manager.get_screen().update,
                    name="VerifyStableZipScreen",
                    key="airgap-button",
                ),
            ]
        )

        mock_schedule_once.assert_has_calls([call(mock_partial(), 0)])
        mock_set_screen.assert_called_once_with(
            name="UnzipStableScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.set_screen")
    def test_on_press_back(self, mock_set_screen, mock_get_locale):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # DO tests
        screen.on_pre_enter()
        action = getattr(VerifyStableZipScreen, f"on_ref_press_{screen.id}")
        action("Mock", "MainScreen")

        # patch assertions
        mock_get_locale.assert_called()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

from unittest.mock import patch, call, MagicMock
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
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
            hasattr(VerifyStableZipScreen, "on_press_verify_stable_zip_screen_button")
        )
        self.assertTrue(
            hasattr(VerifyStableZipScreen, "on_release_verify_stable_zip_screen_button")
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.verify_stable_zip_screen.Sha256Verifyer")
    @patch("src.app.screens.verify_stable_zip_screen.Sha256CheckVerifyer")
    def test_verify_sha256(
        self, mock_check_verifyer, mock_verifyer, mock_get_running_app
    ):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.verify_sha256(assets_dir="mockdir", version="v0.0.1")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

        mock_verifyer.assert_called_once_with(filename="mockdir/krux-v0.0.1.zip")
        mock_check_verifyer.assert_called_once_with(
            filename="mockdir/krux-v0.0.1.zip.sha256.txt"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.verify_stable_zip_screen.SigVerifyer")
    @patch("src.app.screens.verify_stable_zip_screen.PemCheckVerifyer")
    @patch("src.app.screens.verify_stable_zip_screen.SigCheckVerifyer")
    def test_verify_signature(
        self,
        mock_sig_check_verifyer,
        mock_pem_check_verifyer,
        mock_sig_verifyer,
        mock_get_running_app,
    ):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.verify_signature(assets_dir="mockdir", version="v0.0.1")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_pre_enter(self, mock_get_running_app):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.on_pre_enter()

        text = "[size=32sp][color=#efcc00]Verifying integrity and authenticity[/color][/size]"
        self.assertEqual(len(screen.ids["verify_stable_zip_screen_grid"].children), 1)
        self.assertEqual(screen.ids["verify_stable_zip_screen_button"].text, text)
        self.assertTrue(
            hasattr(VerifyStableZipScreen, "on_press_verify_stable_zip_screen_button")
        )
        self.assertTrue(
            hasattr(VerifyStableZipScreen, "on_release_verify_stable_zip_screen_button")
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.manager")
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.get_destdir_assets"
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_sha256"
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_signature"
    )
    def test_on_enter(
        self,
        mock_verify_signature,
        mock_verify_sha256,
        mock_get_destdir_assets,
        mock_manager,
        mock_get_running_app,
    ):
        sha_text = "\n".join(
            [
                "[size=20sp][color=#efcc00]Integrity verification:[/color][/size]",
                "",
                "[size=16sp][b]mockdir/krux-v0.0.1.zip[/b][/size]",
                "[size=14sp][color=#00FF00]mocksha2560123456789abcdef[/color][/size]",
                "",
                "[size=16sp][b]mockdir/krux-v0.0.1.zip.sha256.txt[/b][/size]",
                "[size=14sp][color=#00FF00]mocksha2560123456789abcdef[/color][/size]",
                "[size=14sp]Result: SUCCESS[/b][/size]",
                "",
                "",
            ]
        )

        sig_text = "\n".join(
            [
                "[size=20sp][color=#efcc00]Authenticity verification:[/color][/size]",
                "",
                "[size=16sp]Result: [b]GOOD SIGNATURE[/b][/size]",
                "",
                "[size=16sp]If you have openssl installed on your system[/size]",
                "[size=16sp]you can check manually with the following command:[/size]",
                "",
                "[color=#00ff00][size=14sp]openssl sha256< mockdir/krux-v0.0.1.zip -binary | \\",
                "openssl pkeyutl -verify -pubin -inkey mockdir/selfcustody.pem \\",
                "-sigfile mockdir/krux-v0.0.0.1.zip.sig[/size][/color]",
            ]
        )
        mock_manager.get_screen = MagicMock()
        mock_get_destdir_assets.return_value = "mockdir"
        mock_verify_sha256.return_value = sha_text
        mock_verify_signature.return_value = sig_text

        screen = VerifyStableZipScreen()
        screen.version = "v0.0.1"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.on_pre_enter()
        screen.on_enter()

        full_text = sha_text + sig_text
        self.assertEqual(screen.ids["verify_stable_zip_screen_button"].text, full_text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_verify_sha256.assert_called_once_with(
            assets_dir="mockdir", version=mock_manager.get_screen().version
        )
        mock_verify_signature.assert_called_once_with(
            assets_dir="mockdir", version=mock_manager.get_screen().version
        )

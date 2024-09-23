import os
from unittest.mock import MagicMock, patch, call
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

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.verify_stable_zip_screen.Sha256Verifyer")
    @patch("src.app.screens.verify_stable_zip_screen.Sha256CheckVerifyer")
    def test_verify_sha256(
        self,
        mock_check_verifyer,
        mock_verifyer,
        mock_get_locale,
    ):
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
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.manager")
    def test_on_pre_enter(self, mock_manager, mock_get_locale):
        mock_manager.get_screen = MagicMock()
        mock_manager.get_screen.return_value = MagicMock(version="v0.0.1")
        screen = VerifyStableZipScreen()
        screen.on_pre_enter()
        # self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        text = "".join(
            [
                "[color=#efcc00]",
                "Verifying integrity and authenticity",
                "[/color]",
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
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.build_message_verify_sha256",
        return_value="mock",
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.build_message_verify_signature",
        return_value="mock",
    )
    def test_on_enter(
        self,
        mock_build_message_verify_signature,
        mock_build_message_verify_sha256,
        mock_get_destdir_assets,
        mock_get_locale,
    ):
        screen = VerifyStableZipScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.on_pre_enter()
        screen.on_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.on_pre_enter()
        screen.on_enter()

        # patch assertions
        mock_get_locale.assert_called()
        mock_get_destdir_assets.assert_called()
        mock_build_message_verify_sha256.assert_called_once_with(
            assets_dir="mockdir", version=screen.manager.get_screen().version
        )
        mock_build_message_verify_signature.assert_called_once_with(
            assets_dir="mockdir", version=screen.manager.get_screen().version
        )

    def test_prettyfy_hash(self):
        _hash = "f254692f766dc6b009c8ca7f43b674d088062685bb203b850f8b702f641b5935"
        pretty = VerifyStableZipScreen.prettyfy_hash(_hash)
        expected = "".join(
            [
                "f2   54   69   2f   76   6d   c6   b0   09   c8   ca   7f   43   b6   74   d0",
                "\n",
                "88   06   26   85   bb   20   3b   85   0f   8b   70   2f   64   1b   59   35",
            ]
        )

        self.assertEqual(pretty, expected)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_sha256",
        return_value=tuple(["mockhash", "mockhash", True]),
    )
    def test_build_message_verify_sha256(self, mock_verify_sha256, mock_get_locale):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        p = os.path.join("mock", "krux-v0.0.1.zip")
        expected = "".join(
            [
                "[u]INTEGRITY VERIFICATION[/u]: ",
                "[b][color=#00FF00]SUCCESS[/color][/b]",
                "\n",
                "\n",
                f"[b]computed hash from [color=#777777]{p}[/color][/b]",
                "\n",
                "mo   ck   ha   sh",
                "\n",
                "\n",
                f"[b]provided hash from [color=#777777]{p}.sha256.txt[/color][/b]",
                "\n",
                "mo   ck   ha   sh",
                "\n",
                "\n",
            ]
        )

        actual = screen.build_message_verify_sha256(assets_dir="mock", version="v0.0.1")
        self.assertEqual(actual, expected)
        mock_get_locale.assert_any_call()
        mock_verify_sha256.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_sha256",
        return_value=tuple(["mockhash", "nomockhash", False]),
    )
    def test_failed_build_message_verify_sha256(
        self, mock_verify_sha256, mock_get_locale
    ):
        screen = VerifyStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        p = os.path.join("mock", "krux-v0.0.1.zip")
        expected = "".join(
            [
                "[u]INTEGRITY VERIFICATION[/u]: ",
                "[b][color=#FF0000]FAILED[/color][/b]",
                "\n",
                "\n",
                f"[b]computed hash from [color=#777777]{p}[/color][/b]",
                "\n",
                "mo   ck   ha   sh",
                "\n",
                "\n",
                f"[b]provided hash from [color=#777777]{p}.sha256.txt[/color][/b]",
                "\n",
                "no   mo   ck   ha   sh",
                "\n",
                "\n",
            ]
        )

        actual = screen.build_message_verify_sha256(assets_dir="mock", version="v0.0.1")
        self.assertEqual(actual, expected)
        mock_get_locale.assert_any_call()
        mock_verify_sha256.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_signature",
        return_value=True,
    )
    def test_build_message_verify_signature(self, mock_verify_sig, mock_get_locale):
        screen = VerifyStableZipScreen()
        screen.success = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        p = os.path.join("mock", "krux-v0.0.1.zip")
        s = os.path.join("mock", "selfcustody.pem")
        expected = "".join(
            [
                "[u]AUTHENTICITY VERIFICATION[/u]: ",
                "[b][color=#00FF00]GOOD SIGNATURE[/color][/b]",
                "\n",
                "\n",
                "If you have openssl installed on your system",
                "\n",
                "you can check manually with the following command",
                "\n",
                "\n",
                "[b]",
                f"openssl sha256< [color=#777777]{p}[/color] -binary | \\",
                "\n",
                f"openssl pkeyutl -verify -pubin -inkey [color=#777777]{s}[/color] \\",
                "\n",
                f"-sigfile [color=#777777]{p}.sig[/color]",
                "[/b]",
                "\n",
                "\n",
                "[ref=Proceed][color=#00ff00][u]Proceed[/u][/ref][/color]",
                "             ",
                "[ref=Back][color=#ff0000][u]Back[/u][/ref][/color]",
                "[/b]",
            ]
        )

        actual = screen.build_message_verify_signature(
            assets_dir="mock", version="v0.0.1"
        )

        self.assertEqual(actual, expected)
        mock_get_locale.assert_any_call()
        mock_verify_sig.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_signature",
        return_value=False,
    )
    def test_failed_build_message_verify_signature(
        self, mock_verify_sig, mock_get_locale
    ):
        screen = VerifyStableZipScreen()
        screen.success = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        p = os.path.join("mock", "krux-v0.0.1.zip")
        s = os.path.join("mock", "selfcustody.pem")
        expected = "".join(
            [
                "[u]AUTHENTICITY VERIFICATION[/u]: ",
                "[b][color=#FF0000]BAD SIGNATURE[/color][/b]",
                "\n",
                "\n",
                "If you have openssl installed on your system",
                "\n",
                "you can check manually with the following command",
                "\n",
                "\n",
                "[b]",
                f"openssl sha256< [color=#777777]{p}[/color] -binary | \\",
                "\n",
                f"openssl pkeyutl -verify -pubin -inkey [color=#777777]{s}[/color] \\",
                "\n",
                f"-sigfile [color=#777777]{p}.sig[/color]",
                "[/b]",
                "\n",
                "\n",
                "[ref=Proceed][color=#00ff00][u]Proceed[/u][/ref][/color]",
                "             ",
                "[ref=Back][color=#ff0000][u]Back[/u][/ref][/color]",
                "[/b]",
            ]
        )

        actual = screen.build_message_verify_signature(
            assets_dir="mock", version="v0.0.1"
        )

        print(actual)
        print("========")
        print(expected)
        self.assertEqual(actual, expected)
        mock_get_locale.assert_any_call()
        mock_verify_sig.assert_called_once()

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
        screen.on_pre_enter()
        screen.on_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        # DO tests
        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(None, "Proceed")

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
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.manager")
    @patch("src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.set_screen")
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_sha256",
        return_value=tuple(["mock", "mock", True]),
    )
    @patch(
        "src.app.screens.verify_stable_zip_screen.VerifyStableZipScreen.verify_signature",
        return_value=True,
    )
    def test_on_press_back(
        self,
        mock_verify_signature,
        mock_verify_sha256,
        mock_set_screen,
        mock_manager,
        mock_get_destdir_assets,
        mock_get_locale,
    ):
        mock_manager.get_screen = MagicMock()
        mock_manager.get_screen.return_value = MagicMock(version="v0.0.1")
        screen = VerifyStableZipScreen()
        screen.on_pre_enter()
        screen.on_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        # DO tests
        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(None, "Back")

        # patch assertions
        mock_get_locale.assert_called()
        mock_get_destdir_assets.assert_called()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")
        mock_verify_sha256.assert_called()
        mock_verify_signature.assert_called()

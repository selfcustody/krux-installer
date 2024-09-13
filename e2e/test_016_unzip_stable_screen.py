import os
import sys
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.unzip_stable_screen import (
    UnzipStableScreen,
)


class TestWarningAlreadyDownloadedScreen(GraphicUnitTest):

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
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_init(self, mock_get_destdir_assets, mock_get_locale):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(grid.id, f"{screen.id}_grid")
        self.assertFalse(
            hasattr(UnzipStableScreen, "on_press_unzip_stable_screen_button")
        )
        self.assertFalse(
            hasattr(UnzipStableScreen, "on_release_unzip_stable_screen_button")
        )

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_invalid_name(
        self,
        mock_redirect_exception,
        mock_get_destdir_assets,
        mock_get_locale,
    ):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="MockScreen")

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()
        mock_redirect_exception.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_update_locale(self, mock_get_locale, mock_get_destdir_assets):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_update_version(self, mock_get_locale, mock_get_destdir_assets):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")

        # default assertions
        self.assertEqual(screen.version, "v0.0.1")

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_update_device(self, mock_get_locale, mock_get_destdir_assets):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")

        # default assertions
        self.assertEqual(screen.device, "mock")

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_update_clear(self, mock_get_locale, mock_get_destdir_assets):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.make_button(
            wid=f"{screen.id}_mock_button",
            root_widget=f"{screen.id}_grid",
            text="Mock",
            row=0,
            on_press=MagicMock(),
            on_release=MagicMock(),
        )

        # do tests
        with patch.object(
            screen.ids[f"{screen.id}_grid"], "clear_widgets"
        ) as mock_clear:
            screen.update(name="VerifyStableZipScreen", key="clear")
            mock_clear.assert_called_once()

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_update_flash_button(self, mock_get_locale, mock_get_destdir_assets):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        size = [0, 0]

        if sys.platform in ("linux", "win32"):
            size = [window.size[0] // 24, window.size[0] // 48]

        if sys.platform == "darwin":
            size = [window.size[0] // 48, window.size[0] // 128]

        # do tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="flash-button")

        p = os.path.join("mock", "krux-v0.0.1", "maixpy_mock", "kboot.kfpkg")
        text = "".join(
            [
                f"[size={size[0]}sp]",
                "Flash with",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]",
                "[color=#efcc00]",
                p,
                "[/color]",
                "[/size]",
            ]
        )

        # default assertions
        self.assertEqual(screen.ids[f"{screen.id}_flash_button"].text, text)

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_update_airgap_button(self, mock_get_locale, mock_get_destdir_assets):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        size = [0, 0]

        if sys.platform in ("linux", "win32"):
            size = [window.size[0] // 24, window.size[0] // 48]

        if sys.platform == "darwin":
            size = [window.size[0] // 48, window.size[0] // 128]

        # do tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="airgap-button")

        p = os.path.join("mock", "krux-v0.0.1", "maixpy_mock", "firmware.bin")
        text = "".join(
            [
                f"[size={size[0]}sp]",
                "[color=#333333]",
                "Air-gapped update with (soon)",
                "[/color]",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]",
                "[color=#333333]",
                p,
                "[/color]",
                "[/size]",
            ]
        )

        # default assertions
        self.assertEqual(screen.ids[f"{screen.id}_airgap_button"].text, text)
        self.assertTrue(
            hasattr(UnzipStableScreen, f"on_press_{screen.id}_airgap_button")
        )
        self.assertTrue(
            hasattr(UnzipStableScreen, f"on_release_{screen.id}_airgap_button")
        )

        # patch assertions
        mock_get_destdir_assets.assert_any_call()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    def test_on_press_flash_button(
        self, mock_set_background, mock_get_destdir_assets, mock_get_locale
    ):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        size = [0, 0]

        if sys.platform in ("linux", "win32"):
            size = [window.size[0] // 24, window.size[0] // 48]

        if sys.platform == "darwin":
            size = [window.size[0] // 48, window.size[0] // 128]

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="flash-button")
        button = screen.ids[f"{screen.id}_flash_button"]
        action = getattr(screen, f"on_press_{screen.id}_flash_button")
        action(button)

        p = os.path.join("mock", "krux-v0.0.1", "maixpy_mock", "kboot.kfpkg")
        text = "".join(
            [
                f"[size={size[0]}sp]",
                "Extracting",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]",
                "[color=#efcc00]",
                p,
                "[/color]",
                "[/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()
        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.25, 0.25, 0.25, 1)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    def test_on_press_airgap_button(
        self, mock_set_background, mock_get_destdir_assets, mock_get_locale
    ):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        size = [0, 0]

        if sys.platform in ("linux", "win32"):
            size = [window.size[0] // 24, window.size[0] // 48]

        if sys.platform == "darwin":
            size = [window.size[0] // 48, window.size[0] // 128]

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="airgap-button")
        button = screen.ids[f"{screen.id}_airgap_button"]
        action = getattr(screen, f"on_press_{screen.id}_airgap_button")
        action(button)

        p = os.path.join("mock", "krux-v0.0.1", "maixpy_mock", "firmware.bin")
        text = "".join(
            [
                f"[size={size[0]}sp]",
                "[color=#333333]",
                "Air-gapped update with (soon)",
                "[/color]",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]",
                "[color=#333333]",
                p,
                "[/color]",
                "[/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()
        mock_set_background.assert_not_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.base_screen.BaseScreen.get_baudrate", return_value=1500000)
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    @patch("src.app.screens.unzip_stable_screen.KbootUnzip")
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.manager")
    @patch("src.app.screens.unzip_stable_screen.time.sleep")
    def test_on_release_flash_button(
        self,
        mock_sleep,
        mock_manager,
        mock_kboot_unzip,
        mock_set_background,
        mock_get_baudrate,
        mock_get_destdir_assets,
        mock_get_locale,
    ):
        mock_kboot_unzip.load = MagicMock()
        mock_manager.get_screen = MagicMock()

        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        size = [0, 0]

        if sys.platform in ("linux", "win32"):
            size = [window.size[0] // 24, window.size[0] // 48]

        if sys.platform == "darwin":
            size = [window.size[0] // 48, window.size[0] // 128]

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="flash-button")
        button = screen.ids[f"{screen.id}_flash_button"]
        action = getattr(screen, f"on_release_{screen.id}_flash_button")
        action(button)

        p = os.path.join("mock", "krux-v0.0.1", "maixpy_mock", "kboot.kfpkg")
        text = "".join(
            [
                f"[size={size[0]}sp]",
                "Extracted",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]",
                "[color=#efcc00]",
                p,
                "[/color]",
                "[/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_baudrate.assert_called()
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()
        mock_get_destdir_assets.assert_called_once()
        mock_kboot_unzip.assert_called_once_with(
            filename=os.path.join("mock", "krux-v0.0.1.zip"),
            device="mock",
            output="mock",
        )
        # mock_kboot_unzip.load.assert_called_once()
        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 1))
        mock_manager.get_screen.assert_called_once_with("FlashScreen")
        mock_sleep.assert_called_once_with(2.1)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    # @patch("src.app.screens.unzip_stable_screen.FirmwareUnzip")
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.manager")
    @patch("src.app.screens.unzip_stable_screen.time.sleep")
    def test_on_release_airgapped_button(
        self,
        mock_sleep,
        mock_manager,
        #    mock_firmware_unzip,
        mock_set_background,
        mock_get_destdir_assets,
        mock_get_locale,
    ):
        #    mock_firmware_unzip.load = MagicMock()
        mock_manager.get_screen = MagicMock()

        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        size = [0, 0]

        if sys.platform in ("linux", "win32"):
            size = [window.size[0] // 24, window.size[0] // 48]

        if sys.platform == "darwin":
            size = [window.size[0] // 48, window.size[0] // 128]

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="airgap-button")
        button = screen.ids[f"{screen.id}_airgap_button"]
        action = getattr(screen, f"on_release_{screen.id}_airgap_button")
        action(button)

        p = os.path.join("mock", "krux-v0.0.1", "maixpy_mock", "firmware.bin")
        text = "".join(
            [
                f"[size={size[0]}sp]",
                "[color=#333333]",
                "Air-gapped update with (soon)",
                "[/color]",
                "[/size]",
                "\n",
                f"[size={size[1]}sp]",
                "[color=#333333]",
                p,
                "[/color]",
                "[/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_destdir_assets.assert_called_once()
        mock_get_locale.assert_called()
        #    mock_firmware_unzip.assert_not_called()
        mock_set_background.assert_not_called()
        mock_manager.get_screen.assert_not_called()
        mock_sleep.assert_not_called()

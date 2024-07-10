from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.uix.label import Label
from src.app.screens.unzip_stable_screen import (
    UnzipStableScreen,
)


class TestWarningAlreadyDownloadedScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_invalid_name(self, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="MockScreen")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid screen name: MockScreen")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_key(self, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name=screen.name, key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), 'Invalid key: "mock"')

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_locale(self, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_version(self, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")

        # default assertions
        self.assertEqual(screen.version, "v0.0.1")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_device(self, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")

        # default assertions
        self.assertEqual(screen.device, "mock")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_clear(self, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.make_button(
            id=f"{screen.id}_mock_button",
            root_widget=f"{screen.id}_grid",
            text="Mock",
            markup=True,
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.unzip_stable_screen.UnzipStableScreen.get_destdir_assets",
        return_value="mockdir",
    )
    def test_update_flash_button(self, mock_get_destdir_assets, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="flash-button")
        text = "\n".join(
            [
                "Flash update with",
                "[size=14sp][color=#efcc00]mockdir/krux-v0.0.1/maixpy_mock/kboot.kfpkg[/color][/size]",
            ]
        )

        # default assertions
        self.assertEqual(screen.ids[f"{screen.id}_flash_button"].text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.unzip_stable_screen.UnzipStableScreen.get_destdir_assets",
        return_value="mockdir",
    )
    def test_update_airgap_button(self, mock_get_destdir_assets, mock_get_running_app):
        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="airgap-button")
        text = "\n".join(
            [
                "Airgap update with",
                "[size=14sp][color=#efcc00]mockdir/krux-v0.0.1/maixpy_mock/firmware.bin[/color][/size]",
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.unzip_stable_screen.UnzipStableScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    def test_on_press_flash_button(
        self, mock_set_background, mock_get_destdir_assets, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="flash-button")
        button = screen.ids[f"{screen.id}_flash_button"]
        action = getattr(screen, f"on_press_{screen.id}_flash_button")
        action(button)
        text = "\n".join(
            [
                "Unziping",
                "[size=14sp][color=#efcc00]mockdir/krux-v0.0.1/maixpy_mock/kboot.kfpkg[/color][/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.25, 0.25, 0.25, 1)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.unzip_stable_screen.UnzipStableScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    def test_on_press_airgap_button(
        self, mock_set_background, mock_get_destdir_assets, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="airgap-button")
        button = screen.ids[f"{screen.id}_airgap_button"]
        action = getattr(screen, f"on_press_{screen.id}_airgap_button")
        action(button)
        text = "\n".join(
            [
                "Unziping",
                "[size=14sp][color=#efcc00]mockdir/krux-v0.0.1/maixpy_mock/firmware.bin[/color][/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()
        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.25, 0.25, 0.25, 1)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.unzip_stable_screen.UnzipStableScreen.get_destdir_assets",
        return_value="mockdir",
    )
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
        mock_get_destdir_assets,
        mock_get_running_app,
    ):
        mock_kboot_unzip.load = MagicMock()
        mock_manager.get_screen = MagicMock()
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="flash-button")
        button = screen.ids[f"{screen.id}_flash_button"]
        action = getattr(screen, f"on_release_{screen.id}_flash_button")
        action(button)
        text = "\n".join(
            [
                "Unziped",
                "[size=12sp][color=#efcc00]mockdir/krux-v0.0.1/maixpy_mock/kboot.kfpkg[/color][/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()
        mock_kboot_unzip.assert_called_once_with(
            filename="mockdir/krux-v0.0.1.zip", device="mock", output="mockdir"
        )
        # mock_kboot_unzip.load.assert_called_once()
        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 1))
        mock_manager.get_screen.assert_called_once_with("FlashScreen")
        mock_sleep.assert_called_once_with(2.1)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.unzip_stable_screen.UnzipStableScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.set_background")
    @patch("src.app.screens.unzip_stable_screen.FirmwareUnzip")
    @patch("src.app.screens.unzip_stable_screen.UnzipStableScreen.manager")
    @patch("src.app.screens.unzip_stable_screen.time.sleep")
    def test_on_release_aigap_button(
        self,
        mock_sleep,
        mock_manager,
        mock_firmware_unzip,
        mock_set_background,
        mock_get_destdir_assets,
        mock_get_running_app,
    ):
        mock_firmware_unzip.load = MagicMock()
        mock_manager.get_screen = MagicMock()
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = UnzipStableScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # DO tests
        screen.update(name="VerifyStableZipScreen", key="device", value="mock")
        screen.update(name="VerifyStableZipScreen", key="version", value="v0.0.1")
        screen.update(name="VerifyStableZipScreen", key="airgap-button")
        button = screen.ids[f"{screen.id}_airgap_button"]
        action = getattr(screen, f"on_release_{screen.id}_airgap_button")
        action(button)
        text = "\n".join(
            [
                "Unziped",
                "[size=12sp][color=#efcc00]mockdir/krux-v0.0.1/maixpy_mock/firmware.bin[/color][/size]",
            ]
        )

        # default assertions
        self.assertEqual(button.text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir_assets.assert_called_once()
        mock_firmware_unzip.assert_called_once_with(
            filename="mockdir/krux-v0.0.1.zip", device="mock", output="mockdir"
        )
        # mock_kboot_unzip.load.assert_called_once()
        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 1))
        mock_manager.get_screen.assert_called_once_with("AirgapScreen")
        mock_sleep.assert_called_once_with(2.1)

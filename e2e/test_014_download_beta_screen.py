import os
from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.download_beta_screen import (
    DownloadBetaScreen,
)


class TestDownloadBetaScreen(GraphicUnitTest):

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
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(screen.downloader, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.trigger, None)
        self.assertEqual(screen.firmware, None)
        self.assertEqual(screen.device, None)
        self.assertEqual(screen.to_screen, "FlashScreen")
        self.assertEqual(grid.id, "download_beta_screen_grid")
        self.assertEqual(grid.children[1].id, "download_beta_screen_progress")
        self.assertEqual(grid.children[0].id, "download_beta_screen_info")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_invalid_name(self, mock_redirect_exception, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="MockScreen")

        # patch assertions
        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_firmware(self, mock_redirect_exception, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="firmware", value="mock.kfpkg")

        # patch assertions
        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_firmware(self, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="firmware", value="kboot.kfpkg")

        # default assertions
        self.assertEqual(screen.firmware, "kboot.kfpkg")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_device(self, mock_redirect_exception, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="device", value="mock")

        # default assertions

        # patch assertions
        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_device(self, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="device", value="m5stickv")

        # default assertions
        self.assertEqual(screen.device, "m5stickv")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets",
        return_value="mockdir",
    )
    def test_update_downloader(self, mock_destdir_assets, mock_get_locale):
        screen = DownloadBetaScreen()
        screen.firmware = "kboot.kfpkg"
        screen.device = "amigo"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="downloader")

        firmware_path = os.path.join("mockdir", "krux_binaries", "maixpy_amigo")

        # do tests
        text = "".join(
            [
                "Downloading",
                "\n",
                "[color=#00AABB]",
                "[ref=https://raw.githubusercontent.com/odudex/krux_binaries/main/maixpy_amigo/kboot.kfpkg]",
                "https://raw.githubusercontent.com/odudex/krux_binaries/main/maixpy_amigo/kboot.kfpkg",
                "[/ref]",
                "[/color]",
                "\n",
                "to",
                "\n",
                firmware_path,
                "\n",
            ]
        )
        # default assertions
        self.assertEqual(screen.ids["download_beta_screen_info"].text, text)

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_destdir_assets.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_progress(self, mock_get_locale):
        screen = DownloadBetaScreen()
        screen.downloader = MagicMock(destdir="mockdir")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(
            name="ConfigKruxInstaller",
            key="progress",
            value={"downloaded_len": 210000, "content_len": 21000000},
        )

        # do tests
        text = "".join(
            [
                "[b]1.00 %[/b]",
                "\n",
                "0.20 of 20.03 MB",
            ]
        )

        self.assertEqual(screen.ids["download_beta_screen_progress"].text, text)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_progress_100_percent(self, mock_get_locale):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with (
            patch.object(screen, "trigger") as mock_trigger,
            patch.object(screen, "downloader") as mock_downloader,
        ):

            mock_downloader.destdir = "mockdir"
            screen.update(
                name="ConfigKruxInstaller",
                key="progress",
                value={"downloaded_len": 21000000, "content_len": 21000000},
            )

            # do tests
            text_progress = "".join(
                [
                    "[b]100.00 %[/b]",
                    "\n",
                    "20.03 of 20.03 MB",
                ]
            )

            kboot = os.path.join("mockdir", "kboot.kfpkg")
            text_info = "".join([kboot, "\n", "downloaded"])

            self.assertEqual(
                screen.ids["download_beta_screen_progress"].text, text_progress
            )
            self.assertEqual(screen.ids["download_beta_screen_info"].text, text_info)

            # patch assertions
            mock_get_locale.assert_any_call()
            assert len(mock_trigger.mock_calls) >= 1

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.get_baudrate", return_value=1500000)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch("src.app.screens.download_beta_screen.time.sleep")
    @patch("src.app.screens.download_beta_screen.DownloadBetaScreen.manager")
    @patch("src.app.screens.download_beta_screen.partial")
    @patch("src.app.screens.download_beta_screen.Clock.schedule_once")
    @patch("src.app.screens.download_beta_screen.DownloadBetaScreen.set_screen")
    def test_on_trigger(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_manager,
        mock_sleep,
        mock_get_destdir_assets,
        mock_get_baudrate,
        mock_get_locale,
    ):
        # Mocks
        mock_manager.get_screen = MagicMock()

        # screen
        screen = DownloadBetaScreen()
        screen.baudrate = 1500000
        screen.device = "amigo"
        screen.firmware = "kboot.kfpkg"

        # pylint: disable=no-member
        screen.trigger = screen.on_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        # pylint: disable=no-member
        DownloadBetaScreen.on_trigger(0)

        # default assertions
        self.assertFalse(screen.on_trigger is None)
        self.assertFalse(screen.trigger is None)

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_get_destdir_assets.assert_any_call()
        mock_get_baudrate.assert_any_call()
        mock_sleep.assert_called_once_with(2.1)
        mock_manager.get_screen.assert_called_once_with("FlashScreen")

        p = os.path.join(
            "mockdir",
            "krux_binaries",
            "maixpy_amigo",
            "kboot.kfpkg",
        )
        mock_partial.assert_has_calls(
            [
                call(
                    mock_manager.get_screen().update,
                    name=screen.name,
                    key="baudrate",
                    value=1500000,
                ),
                call(
                    mock_manager.get_screen().update,
                    name=screen.name,
                    key="firmware",
                    value=p,
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 0)]
        )
        mock_set_screen.assert_called_once_with(name="FlashScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.download_beta_screen.partial")
    def test_on_progress(self, mock_partial, mock_get_locale):

        # screen
        screen = DownloadBetaScreen()
        screen.baudrate = 1500000
        screen.device = "amigo"
        screen.firmware = "kboot.kfpkg"

        # pylint: disable=no-member
        screen.trigger = screen.on_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        # pylint: disable=no-member
        with patch.object(screen, "downloader") as mock_downloader:
            mock_downloader.downloaded_len = 21
            mock_downloader.content_len = 21000000
            DownloadBetaScreen.on_progress(data=[])

            # default assertions
            self.assertFalse(screen.on_progress is None)

            # patch assertions
            mock_get_locale.assert_any_call()
            mock_partial.assert_has_calls(
                [
                    call(
                        screen.update,
                        name=screen.name,
                        key="progress",
                        value={"downloaded_len": 21, "content_len": 21000000},
                    ),
                ]
            )

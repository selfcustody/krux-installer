import os
import sys
from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.download_beta_screen import (
    DownloadBetaScreen,
)


class TestDownloadBetaScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_invalid_name(self, mock_get_running_app):
        screen = DownloadBetaScreen()
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
        screen = DownloadBetaScreen()
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
        screen = DownloadBetaScreen()
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
    def test_fail_update_firmware(self, mock_get_running_app):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name=screen.name, key="firmware", value="mock.kfpkg")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid firmware: mock.kfpkg")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_firmware(self, mock_get_running_app):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="firmware", value="kboot.kfpkg")

        # default assertions
        self.assertEqual(screen.firmware, "kboot.kfpkg")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_device(self, mock_get_running_app):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name=screen.name, key="device", value="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid device: mock")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_device(self, mock_get_running_app):
        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="device", value="m5stickv")

        # default assertions
        self.assertEqual(screen.device, "m5stickv")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets",
        return_value="mockdir",
    )
    def test_update_downloader(self, mock_get_destdir, mock_get_running_app):
        screen = DownloadBetaScreen()
        screen.firmware = "kboot.kfpkg"
        screen.device = "amigo"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_mp = window.size[0] // 128

        # do tests
        screen.update(name=screen.name, key="downloader")

        firmware_path = os.path.join("mockdir", "krux_binaries", "maixpy_amigo")

        # do tests
        text = "\n".join(
            [
                f"[size={fontsize_mp}sp]" "Downloading",
                "".join(
                    [
                        "[color=#00AABB][ref=https://raw.githubusercontent.com/odudex",
                        "/krux_binaries/main/maixpy_amigo/kboot.kfpkg]https://raw.githubusercontent",
                        ".com/odudex/krux_binaries/main/maixpy_amigo/kboot.kfpkg[/ref][/color]",
                    ]
                ),
                f"to {firmware_path}",
                "[/size]",
            ]
        )
        # default assertions
        self.assertEqual(screen.ids["download_beta_screen_info"].text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_get_destdir.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_progress(self, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        fontsize_g = 0
        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_g = window.size[0] // 16
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_g = window.size[0] // 32
            fontsize_mp = window.size[0] // 128

        # do tests
        screen.update(
            name="ConfigKruxInstaller",
            key="progress",
            value={"downloaded_len": 210000, "content_len": 21000000},
        )

        # do tests
        text = "\n".join(
            [
                f"[size={fontsize_g}sp][b]1.00 %[/b][/size]",
                "",
                f"[size={fontsize_mp}sp]0.20 of 20.03 MB[/size]",
            ]
        )

        self.assertEqual(screen.ids["download_beta_screen_progress"].text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_progress_100_percent(self, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = DownloadBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        fontsize_g = 0
        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_g = window.size[0] // 16
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_g = window.size[0] // 32
            fontsize_mp = window.size[0] // 128

        # do tests
        with patch.object(screen, "trigger") as mock_trigger, patch.object(
            screen, "downloader"
        ) as mock_downloader:

            mock_downloader.destdir = "mockdir"
            screen.update(
                name="ConfigKruxInstaller",
                key="progress",
                value={"downloaded_len": 21000000, "content_len": 21000000},
            )

            # do tests
            text_progress = "\n".join(
                [
                    f"[size={fontsize_g}sp][b]100.00 %[/b][/size]",
                    "",
                    f"[size={fontsize_mp}sp]20.03 of 20.03 MB[/size]",
                ]
            )

            text_info = "\n".join(
                [f"[size={fontsize_mp}sp]", "mockdir/kboot.kfpkg downloaded", "[/size]"]
            )

            self.assertEqual(
                screen.ids["download_beta_screen_progress"].text, text_progress
            )
            self.assertEqual(screen.ids["download_beta_screen_info"].text, text_info)

            # patch assertions
            mock_get_running_app.assert_has_calls(
                [call().config.get("locale", "lang")],
                any_order=True,
            )

            assert len(mock_trigger.mock_calls) >= 1

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
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
        mock_get_running_app,
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )
        mock_sleep.assert_called_once_with(2.1)
        mock_manager.get_screen.assert_called_once_with("FlashScreen")

        p = os.path.join(
            mock_get_running_app().config.get(),
            "krux_binaries",
            "maixpy_amigo",
            "kboot.kfpkg",
        )
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    mock_manager.get_screen().update,
                    name=screen.name,
                    key="baudrate",
                    value=1,
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
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.download_beta_screen.partial")
    @patch("src.app.screens.download_beta_screen.Clock.schedule_once")
    def test_on_progress(
        self,
        mock_schedule_once,
        mock_partial,
        mock_get_running_app,
    ):

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
            mock_get_running_app.assert_has_calls(
                [call().config.get("locale", "lang")],
                any_order=True,
            )

            mock_partial.assert_has_calls(
                [
                    call(screen.update, name=screen.name, key="canvas"),
                    call(
                        screen.update,
                        name=screen.name,
                        key="progress",
                        value={"downloaded_len": 21, "content_len": 21000000},
                    ),
                ]
            )
            mock_schedule_once.assert_has_calls(
                [call(mock_partial(), 0), call(mock_partial(), 0)], any_order=True
            )

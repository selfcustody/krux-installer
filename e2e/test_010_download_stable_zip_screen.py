import os
import sys
from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.download_stable_zip_screen import DownloadStableZipScreen


class TestDownloadStableZipScreen(GraphicUnitTest):

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
    def test_init(self, mock_get_locale):
        screen = DownloadStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(screen.downloader, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.trigger, None)
        self.assertEqual(screen.version, None)
        self.assertEqual(screen.to_screen, "DownloadStableZipSha256Screen")
        self.assertEqual(grid.id, "download_stable_zip_screen_grid")
        self.assertEqual(grid.children[1].id, "download_stable_zip_screen_progress")
        self.assertEqual(grid.children[0].id, "download_stable_zip_screen_info")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_invalid_name(
        self,
        mock_redirect_excpetion,
        mock_get_locale,
    ):
        screen = DownloadStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="MockScreen")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_redirect_excpetion.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = DownloadStableZipScreen()
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
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets",
        return_value="mockdir",
    )
    @patch("src.app.screens.download_stable_zip_screen.ZipDownloader")
    def test_update_version(
        self,
        mock_downloader,
        mock_get_destdir_assets,
        mock_get_locale,
    ):

        screen = DownloadStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests

        screen.update(name="ConfigKruxInstaller", key="version", value="v0.0.1")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_get_destdir_assets.assert_any_call()
        mock_downloader.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_progress(self, mock_get_locale):
        screen = DownloadStableZipScreen()
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
        text = "".join(
            [
                f"[size={fontsize_g}sp][b]1.00 %[/b][/size]",
                "\n",
                f"[size={fontsize_mp}sp]",
                "0.20",
                " of ",
                "20.03 MB",
                "[/size]",
            ]
        )

        self.assertEqual(screen.ids["download_stable_zip_screen_progress"].text, text)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_progress_100_percent(self, mock_get_locale):
        screen = DownloadStableZipScreen()
        screen.version = "v24.07.0"
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
            text_progress = "".join(
                [
                    f"[size={fontsize_g}sp][b]100.00 %[/b][/size]",
                    "\n",
                    f"[size={fontsize_mp}sp]",
                    "20.03",
                    " of ",
                    "20.03",
                    " MB",
                    "[/size]",
                ]
            )

            filepath = os.path.join("mockdir", "krux-v24.07.0.zip")
            text_info = "".join(
                [
                    f"[size={fontsize_mp}sp]",
                    filepath,
                    "\n",
                    "downloaded",
                    "[/size]",
                ]
            )

            self.assertEqual(
                screen.ids["download_stable_zip_screen_progress"].text, text_progress
            )
            self.assertEqual(
                screen.ids["download_stable_zip_screen_info"].text, text_info
            )

            # patch assertions
            mock_get_locale.assert_any_call()
            assert len(mock_trigger.mock_calls) >= 1

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.download_stable_zip_screen.ZipDownloader")
    @patch("src.app.screens.download_stable_zip_screen.partial")
    @patch("src.app.screens.download_stable_zip_screen.Clock.schedule_once")
    def test_on_progress(
        self,
        mock_schedule_once,
        mock_partial,
        mock_downloader,
        mock_get_locale,
    ):

        mock_downloader.downloaded_len = 8
        mock_downloader.content_len = 21000000

        # screen
        screen = DownloadStableZipScreen()
        screen.downloader = mock_downloader
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        # pylint: disable=no-member
        DownloadStableZipScreen.on_progress(data=b"")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    screen.update,
                    name=screen.name,
                    key="progress",
                    value={"downloaded_len": 8, "content_len": 21000000},
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 0)]
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.download_stable_zip_screen.time.sleep")
    @patch("src.app.screens.download_stable_zip_screen.DownloadStableZipScreen.manager")
    @patch("src.app.screens.download_stable_zip_screen.partial")
    @patch("src.app.screens.download_stable_zip_screen.Clock.schedule_once")
    @patch(
        "src.app.screens.download_stable_zip_screen.DownloadStableZipScreen.set_screen"
    )
    def test_on_trigger(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_manager,
        mock_sleep,
        mock_get_locale,
    ):
        # Mocks
        mock_manager.get_screen = MagicMock()

        # screen
        screen = DownloadStableZipScreen()
        screen.version = "v0.0.1"

        # pylint: disable=no-member
        screen.trigger = screen.on_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        # pylint: disable=no-member
        DownloadStableZipScreen.on_trigger(0)

        # default assertions
        self.assertFalse(screen.on_trigger is None)
        self.assertFalse(screen.trigger is None)

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_sleep.assert_called_once_with(2.1)
        mock_manager.get_screen.assert_called_once_with("DownloadStableZipSha256Screen")
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    mock_manager.get_screen().update,
                    name=screen.name,
                    key="version",
                    value="v0.0.1",
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 0)]
        )
        mock_set_screen.assert_called_once_with(
            name="DownloadStableZipSha256Screen", direction="left"
        )

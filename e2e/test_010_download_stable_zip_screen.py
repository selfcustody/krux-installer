from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.download_stable_zip_screen import DownloadStableZipScreen


class TestDownloadStableZipScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_invalid_name(self, mock_get_running_app):
        screen = DownloadStableZipScreen()
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
        screen = DownloadStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="ConfigKruxInstaller", key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), 'Invalid key: "mock"')

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_locale(self, mock_get_running_app):
        screen = DownloadStableZipScreen()
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
    @patch("src.app.screens.download_stable_zip_screen.ZipDownloader")
    def test_update_version(self, mock_downloader, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = DownloadStableZipScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests

        screen.update(name="ConfigKruxInstaller", key="version", value="v0.0.1")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [
                call().config.get("locale", "lang"),
                call().config.get("destdir", "assets"),
            ],
            any_order=True,
        )
        mock_downloader.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_progress(self, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = DownloadStableZipScreen()
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
        text = "\n".join(
            [
                "[size=100sp][b]1.00 %[/b][/size]",
                "",
                "[size=16sp]0.20 of 20.03 MB[/size]",
            ]
        )

        self.assertEqual(screen.ids["download_stable_zip_screen_progress"].text, text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.download_stable_zip_screen.ZipDownloader")
    @patch("src.app.screens.download_stable_zip_screen.partial")
    @patch("src.app.screens.download_stable_zip_screen.Clock.schedule_once")
    def test_on_progress(
        self, mock_schedule_once, mock_partial, mock_downloader, mock_get_running_app
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

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
    @patch("src.app.screens.base_screen.App.get_running_app")
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
        mock_get_running_app,
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
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )
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

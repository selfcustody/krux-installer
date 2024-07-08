from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.download_selfcustody_pem_screen import (
    DownloadSelfcustodyPemScreen,
)


class TestDownloadSelfcustodyPemScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(screen.downloader, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.trigger, None)
        self.assertEqual(screen.to_screen, "VerifyStableZipScreen")
        self.assertEqual(grid.id, "download_selfcustody_pem_screen_grid")
        self.assertEqual(
            grid.children[1].id, "download_selfcustody_pem_screen_progress"
        )
        self.assertEqual(grid.children[0].id, "download_selfcustody_pem_screen_info")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_invalid_name(self, mock_get_running_app):
        screen = DownloadSelfcustodyPemScreen()
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
        screen = DownloadSelfcustodyPemScreen()
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
        screen = DownloadSelfcustodyPemScreen()
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
    @patch("src.app.screens.download_selfcustody_pem_screen.PemDownloader")
    def test_update_public_key_certificate(self, mock_downloader, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = DownloadSelfcustodyPemScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name=screen.name, key="public-key-certificate")

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

        screen = DownloadSelfcustodyPemScreen()
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
                "[size=16sp]210000 of 21000000 B[/size]",
            ]
        )

        self.assertEqual(
            screen.ids["download_selfcustody_pem_screen_progress"].text, text
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.download_selfcustody_pem_screen.PemDownloader")
    @patch("src.app.screens.download_selfcustody_pem_screen.partial")
    @patch("src.app.screens.download_selfcustody_pem_screen.Clock.schedule_once")
    def test_on_progress(
        self, mock_schedule_once, mock_partial, mock_downloader, mock_get_running_app
    ):

        mock_downloader.downloaded_len = 8
        mock_downloader.content_len = 21000000

        # screen
        screen = DownloadSelfcustodyPemScreen()
        screen.downloader = mock_downloader
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        # pylint: disable=no-member
        DownloadSelfcustodyPemScreen.on_progress(data=b"")

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
    @patch("src.app.screens.download_selfcustody_pem_screen.time.sleep")
    @patch(
        "src.app.screens.download_selfcustody_pem_screen.DownloadSelfcustodyPemScreen.set_screen"
    )
    def test_on_trigger(
        self,
        mock_set_screen,
        mock_sleep,
        mock_get_running_app,
    ):
        # screen
        screen = DownloadSelfcustodyPemScreen()

        # pylint: disable=no-member
        screen.trigger = screen.on_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        # pylint: disable=no-member
        DownloadSelfcustodyPemScreen.on_trigger(0)

        # default assertions
        self.assertFalse(screen.on_trigger is None)
        self.assertFalse(screen.trigger is None)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )
        mock_sleep.assert_called_once_with(2.1)
        mock_set_screen.assert_called_once_with(
            name="VerifyStableZipScreen", direction="left"
        )

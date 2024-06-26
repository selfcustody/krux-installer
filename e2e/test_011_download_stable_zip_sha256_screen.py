import io
from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.download_stable_zip_sha256_screen import (
    DownloadStableZipSha256Screen,
)


class TestDownloadStableZipSha256Screen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
        screen = DownloadStableZipSha256Screen()
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
        self.assertEqual(screen.to_screen, "DownloadStableZipSigScreen")
        self.assertEqual(grid.id, "download_stable_zip_sha256_screen_grid")
        self.assertEqual(
            grid.children[1].id, "download_stable_zip_sha256_screen_label_progress"
        )
        self.assertEqual(
            grid.children[0].id, "download_stable_zip_sha256_screen_label_info"
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_invalid_name(self, mock_get_running_app):
        screen = DownloadStableZipSha256Screen()
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
        screen = DownloadStableZipSha256Screen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="DownloadStableZipScreen", key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), 'Invalid key: "mock"')

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_locale(self, mock_get_running_app):
        screen = DownloadStableZipSha256Screen()
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
    @patch("src.app.screens.download_stable_zip_sha256_screen.Sha256Downloader")
    def test_update_version(self, mock_downloader, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = DownloadStableZipSha256Screen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="DownloadStableZipScreen", key="version", value="v0.0.1")

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
    @patch(
        "src.app.screens.download_stable_zip_sha256_screen.DownloadStableZipSha256Screen.manager"
    )
    @patch("src.app.screens.download_stable_zip_sha256_screen.partial")
    @patch("src.app.screens.download_stable_zip_sha256_screen.Clock.schedule_once")
    @patch(
        "src.app.screens.download_stable_zip_sha256_screen.DownloadStableZipSha256Screen.set_screen"
    )
    def test_on_trigger(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_manager,
        mock_get_running_app,
    ):
        # Mocks
        mock_manager.get_screen = MagicMock()

        # screen
        screen = DownloadStableZipSha256Screen()
        screen.version = "v0.0.1"

        # pylint: disable=no-member
        screen.trigger = screen.on_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        # pylint: disable=no-member
        DownloadStableZipSha256Screen.on_trigger(0)

        # default assertions
        self.assertFalse(screen.on_trigger is None)
        self.assertFalse(screen.trigger is None)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )
        mock_manager.get_screen.assert_called_once_with("DownloadStableZipSigScreen")
        mock_partial.assert_called_once()
        mock_schedule_once.assert_called_once()
        mock_set_screen.assert_called_once_with(
            name="DownloadStableZipSigScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_progress(self, mock_get_running_app):
        # mock
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # screen
        screen = DownloadStableZipSha256Screen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        text = "\n".join(
            ["[size=100sp][b]2.24%[/b][/size]", "[size=16sp]0.00 of 0.00 MB[/size]"]
        )

        # default assertions
        with patch(
            "src.app.screens.download_stable_zip_sha256_screen.DownloadStableZipSha256Screen.downloader"
        ) as mock_downloader:
            mock_downloader.downloaded_len = 8
            mock_downloader.content_len = file.getbuffer().nbytes

            # pylint: disable=no-member
            DownloadStableZipSha256Screen.on_progress(data=bytes(file.read(8)))
            self.assertEqual(
                screen.ids["download_stable_zip_sha256_screen_label_progress"].text,
                text,
            )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch(
        "src.app.screens.download_stable_zip_sha256_screen.time.sleep",
        side_effect=[True],
    )
    def test_on_progress_done(self, mock_sleep, mock_get_running_app):
        # mock
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # screen
        screen = DownloadStableZipSha256Screen()
        screen.version = "v0.0.1"
        screen.trigger = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        text_progress = "\n".join(
            ["[size=100sp][b]100.00%[/b][/size]", "[size=16sp]0.00 of 0.00 MB[/size]"]
        )
        text_label = "tmpmock/krux-v0.0.1.zip downloaded"

        # default assertions
        with patch(
            "src.app.screens.download_stable_zip_sha256_screen.DownloadStableZipSha256Screen.downloader"
        ) as mock_downloader:
            mock_downloader.destdir = "tmpmock"
            mock_downloader.downloaded_len = file.getbuffer().nbytes
            mock_downloader.content_len = file.getbuffer().nbytes

            # pylint: disable=no-member
            DownloadStableZipSha256Screen.on_progress(data=bytes(file.read(8)))
            self.assertEqual(
                screen.ids["download_stable_zip_sha256_screen_label_progress"].text,
                text_progress,
            )
            self.assertEqual(
                screen.ids["download_stable_zip_sha256_screen_label_info"].text,
                text_label,
            )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_sleep.assert_called_once_with(2.1)

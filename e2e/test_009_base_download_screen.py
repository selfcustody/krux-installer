import os
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.base_download_screen import BaseDownloadScreen


class TestBaseDownloadScreen(GraphicUnitTest):

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
    def test_init(
        self,
        mock_get_locale,
    ):
        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        setattr(screen, "update", MagicMock())
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
        self.assertEqual(screen.to_screen, "AnotherMockScreen")
        self.assertEqual(grid.id, "mock_screen_grid")
        self.assertEqual(grid.children[1].id, "mock_screen_progress")
        self.assertEqual(grid.children[0].id, "mock_screen_info")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_download_screen.Clock.create_trigger")
    def test_set_trigger(self, mock_create_trigger, mock_get_locale):
        mock_trigger = MagicMock()

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.trigger = mock_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        self.assertFalse(screen.trigger is None)

        # patch assertions
        mock_create_trigger.assert_called()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_set_thread(self, mock_get_locale):
        mock_target = MagicMock()

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.thread = MagicMock(name="mock", target=mock_target)
        setattr(screen, "update", MagicMock())
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        self.assertFalse(screen.thread is None)

        # patch tests
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_pre_enter(self, mock_get_locale):
        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        setattr(screen, "update", MagicMock())
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.on_pre_enter()
        text = "".join(
            [
                "Connecting...",
            ]
        )

        self.assertTrue("mock_screen_progress" in screen.ids)
        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_on_enter(self, mock_redirect_exception, mock_get_locale):

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.downloader = None
        setattr(screen, "update", MagicMock())
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.on_enter()

        # default assertions
        self.assertTrue(screen.trigger is None)
        self.assertTrue(screen.thread is None)

        # patch tests
        mock_get_locale.assert_any_call()
        mock_redirect_exception.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_download_screen.partial")
    @patch("src.app.screens.base_download_screen.Clock.create_trigger")
    @patch("src.app.screens.base_download_screen.Thread.start")
    def test_on_enter(
        self,
        mock_thread,
        mock_create_trigger,
        mock_partial,
        mock_get_locale,
    ):
        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        setattr(BaseDownloadScreen, "on_trigger", MagicMock())
        # pylint: disable=no-member
        BaseDownloadScreen.on_trigger.return_value = True

        setattr(BaseDownloadScreen, "on_progress", MagicMock())

        # pylint: disable=no-member
        BaseDownloadScreen.on_progress.return_value = True
        screen.downloader = MagicMock()

        screen.on_enter()

        # patch tests
        mock_get_locale.assert_any_call()

        on_progress = getattr(BaseDownloadScreen, "on_progress")
        mock_partial.assert_called_once_with(
            screen.downloader.download, on_data=on_progress
        )
        mock_create_trigger.assert_called()
        mock_thread.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_download_screen_version(self, mock_get_locale):
        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        build_downloader = MagicMock()
        setattr(screen, "build_downloader", build_downloader)
        setattr(screen, "update", MagicMock())
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update_download_screen(key="version", value="0.0.1")

        mock_get_locale.assert_any_call()
        build_downloader.assert_called_once_with("0.0.1")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_download_screen_progress(self, mock_get_locale):
        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        on_download_progress = MagicMock()
        setattr(screen, "on_download_progress", on_download_progress)
        setattr(screen, "update", MagicMock())
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update_download_screen(key="progress", value="mock")

        mock_get_locale.assert_any_call()
        on_download_progress.assert_called_once_with("mock")

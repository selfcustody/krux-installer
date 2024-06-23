from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.base_download_screen import BaseDownloadScreen


class TestBaseDownloadScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
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
        self.assertEqual(grid.children[1].id, "mock_screen_label_progress")
        self.assertEqual(grid.children[0].id, "mock_screen_label_info")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.base_download_screen.Clock.create_trigger")
    def test_set_trigger(self, mock_create_trigger, mock_get_running_app):
        mock_trigger = MagicMock()

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.trigger = mock_trigger
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        self.assertFalse(screen.trigger is None)

        # patch tests
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        assert mock_create_trigger.called

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.base_download_screen.Thread")
    def test_set_thread(self, mock_thread, mock_get_running_app):
        mock_func = MagicMock()

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.thread = mock_func
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        self.assertFalse(screen.thread is None)

        # patch tests
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_thread.assert_called_once_with(name=screen.name, target=mock_func)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_on_enter(self, mock_get_running_app):

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.downloader = None
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.on_enter()

        # default assertions
        self.assertEqual(
            str(exc_info.exception),
            "Downloader isnt configured. Use `update` method first",
        )
        self.assertTrue(screen.trigger is None)
        self.assertTrue(screen.thread is None)

        # patch tests
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.base_download_screen.Clock.create_trigger")
    @patch("src.app.screens.base_download_screen.Thread")
    def test_on_enter(self, mock_thread, mock_create_trigger, mock_get_running_app):

        screen = BaseDownloadScreen(wid="mock_screen", name="MockScreen")
        screen.to_screen = "AnotherMockScreen"
        screen.downloader = MagicMock()
        screen.downloader.download = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.on_enter()

        # default assertions
        self.assertFalse(screen.trigger is None)
        self.assertFalse(screen.thread is None)

        # patch tests
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        assert mock_create_trigger.called
        mock_thread.assert_called_once_with(
            name=screen.name, target=screen.downloader.download
        )

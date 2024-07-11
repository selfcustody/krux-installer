from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.base_flash_screen import BaseFlashScreen


class TestBaseFlashScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(grid.id, "mock_screen_grid")
        self.assertEqual(len(grid.children), 0)
        self.assertEqual(screen.firmware, None)
        self.assertEqual(screen.baudrate, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.trigger, None)
        self.assertEqual(screen.output, None)
        self.assertEqual(screen.progress, None)
        self.assertEqual(screen.is_done, False)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.base_flash_screen.os.path.exists", side_effect=[True])
    def test_set_firmware(self, mock_exists, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.firmware = "mockpath/kboot.kfpkg"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_exists.assert_called_once_with("mockpath/kboot.kfpkg")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.base_flash_screen.os.path.exists", side_effect=[False])
    def test_fail_set_firmware(self, mock_exists, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.firmware = "mockpath/kboot.kfpkg"

        # default assertions
        self.assertEqual(
            str(exc_info.exception), "Firmware not exist: mockpath/kboot.kfpkg"
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_exists.assert_called_once_with("mockpath/kboot.kfpkg")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_set_baudrate(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.baudrate = "1500000"

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_set_thread(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.thread = MagicMock()

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_set_trigger(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.trigger = MagicMock()

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_set_output(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.output = ["magic", "mock"]

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        self.assertEqual(len(screen.output), 2)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_set_progress(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.progress = ""

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_set_is_done(self, mock_get_running_app):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.is_done = True

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

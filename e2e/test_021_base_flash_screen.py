from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.base_flash_screen import BaseFlashScreen


class TestBaseFlashScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
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
        self.assertEqual(screen.is_done, False)
        self.assertEqual(screen.done, None)
        self.assertEqual(screen.output, [])

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_flash_screen.os.path.exists", side_effect=[True])
    def test_set_firmware(self, mock_exists, mock_get_locale):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.firmware = "mock.kfpkg"
        self.assertEqual(screen.firmware, "mock.kfpkg")

        mock_exists.assert_called_once_with("mock.kfpkg")

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_flash_screen.os.path.exists", side_effect=[False])
    def test_fail_set_firmware(self, mock_exists, mock_get_locale):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")

        with self.assertRaises(ValueError) as exc_info:
            screen.firmware = "mock.kfpkg"

        self.assertEqual(str(exc_info.exception), "Firmware not exist: mock.kfpkg")
        # patch assertions
        mock_get_locale.assert_called()
        mock_exists.assert_called_once_with("mock.kfpkg")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_set_baudrate(self, mock_get_locale):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.baudrate = "1500000"
        self.assertEqual(screen.baudrate, "1500000")

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_set_thread(self, mock_get_locale):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.thread = MagicMock()
        screen.thread.start = MagicMock()

        screen.thread.start()
        screen.thread.start.assert_called_once()

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_flash_screen.Clock.create_trigger")
    def test_set_done(self, mock_create_trigger, mock_get_locale):
        mock_trigger = MagicMock()
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.done = mock_trigger

        # patch assertions
        mock_get_locale.assert_called()
        mock_create_trigger.assert_has_calls([call(mock_trigger)], any_order=True)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_set_output(self, mock_get_locale):
        screen = BaseFlashScreen(wid="mock_screen", name="MockScreen")
        screen.output = ["mock", "this", "test"]
        self.assertEqual(len(screen.output), 3)

        # patch assertions
        mock_get_locale.assert_called()

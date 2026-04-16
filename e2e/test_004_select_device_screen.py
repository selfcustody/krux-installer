from unittest.mock import MagicMock, call, patch

from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest

from src.app.screens.select_device_screen import SelectDeviceScreen


class TestSelectDeviceScreen(GraphicUnitTest):
    @classmethod
    def teardown_class(cls):
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectDeviceScreen")
        self.assertEqual(screen.id, "select_device_screen")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_grid_layout(self, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_device_screen_grid")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_buttons(self, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 10)
        self.assertEqual(buttons[9].id, "select_device_m5stickv")
        self.assertEqual(buttons[8].id, "select_device_amigo")
        self.assertEqual(buttons[7].id, "select_device_dock")
        self.assertEqual(buttons[6].id, "select_device_bit")
        self.assertEqual(buttons[5].id, "select_device_yahboom")
        self.assertEqual(buttons[4].id, "select_device_cube")
        self.assertEqual(buttons[3].id, "select_device_wonder_mv")
        self.assertEqual(buttons[2].id, "select_device_tzt")
        self.assertEqual(buttons[1].id, "select_device_embed_fire")
        self.assertEqual(buttons[0].id, "select_device_wonder_k")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_all_devices_enabled(self, mock_set_background, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        for button in grid.children:
            action = getattr(screen.__class__, f"on_press_{button.id}")
            action(button)

        mock_set_background.assert_called()
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_goes_to_main_screen(
        self, mock_set_screen, mock_manager, mock_get_locale
    ):
        mock_manager.get_screen = MagicMock()
        screen = SelectDeviceScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        for button in grid.children:
            action = getattr(screen.__class__, f"on_release_{button.id}")
            action(button)

        mock_set_screen.assert_called()
        for c in mock_set_screen.call_args_list:
            self.assertEqual(c, call(name="MainScreen", direction="right"))
        mock_get_locale.assert_called_once()

from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.select_device_screen import SelectDeviceScreen


class TestSelectDeviceScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectDeviceScreen")
        self.assertEqual(screen.id, "select_device_screen")

        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_grid_layout(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_device_screen_grid")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_buttons(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 6)
        self.assertEqual(buttons[5].id, "select_device_m5stickv")
        self.assertEqual(buttons[4].id, "select_device_amigo")
        self.assertEqual(buttons[3].id, "select_device_dock")
        self.assertEqual(buttons[2].id, "select_device_bit")
        self.assertEqual(buttons[1].id, "select_device_yahboom")
        self.assertEqual(buttons[0].id, "select_device_cube")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_fail_update(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        with self.assertRaises(ValueError) as exc_info:
            screen.update(key="mock", value="mock")

        self.assertEqual(str(exc_info.exception), "Invalid key: mock")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_latest_version(
        self, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(key="version", value="v24.03.0")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
            ):
                calls.append(call(wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_v23_08_1_version(
        self, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(key="version", value="v23.09.1")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
            ):
                calls.append(call(wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_v22_03_0_version(
        self, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(key="version", value="v22.03.0")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen, f"on_press_{button.id}")
            action(button)
            if button.id in ("select_device_m5stickv"):
                calls.append(call(wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_beta_version(
        self, mock_set_background, mock_get_running_app
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(key="version", value="odudex/krux_binaries")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
                "select_device_cube",
            ):
                calls.append(call(wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_with_latest_version(
        self, mock_set_screen, mock_manager, mock_set_background, mock_get_running_app
    ):
        mock_manager.get_screen = MagicMock()

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        screen.update(key="version", value="v24.03.0")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_manager = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen, f"on_release_{button.id}")
            action(button)

            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 0)))
                calls_manager.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_with_beta_version(
        self, mock_set_screen, mock_manager, mock_set_background, mock_get_running_app
    ):
        mock_manager.get_screen = MagicMock()

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        screen.update(key="version", value="odudex/krux_binaries")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_manager = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen, f"on_release_{button.id}")
            action(button)

            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
                "select_device_cube",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 0)))
                calls_manager.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_with_v22_03_0_version(
        self, mock_set_screen, mock_manager, mock_set_background, mock_get_running_app
    ):
        mock_manager.get_screen = MagicMock()

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = SelectDeviceScreen()
        screen.update(key="version", value="v22.03.0")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_manager = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen, f"on_release_{button.id}")
            action(button)

            if button.id in ("select_device_m5stickv"):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 0)))
                calls_manager.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_running_app.assert_called_once()

from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from src.app.screens.select_device_screen import SelectDeviceScreen


class TestSelectDeviceScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        # Unschedule all pending Clock events to prevent race conditions
        # with subsequent tests
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

        # get your Window instance safely
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

        # get your Window instance safely
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

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 9)
        self.assertEqual(buttons[8].id, "select_device_m5stickv")
        self.assertEqual(buttons[7].id, "select_device_amigo")
        self.assertEqual(buttons[6].id, "select_device_dock")
        self.assertEqual(buttons[5].id, "select_device_bit")
        self.assertEqual(buttons[4].id, "select_device_yahboom")
        self.assertEqual(buttons[3].id, "select_device_cube")
        self.assertEqual(buttons[2].id, "select_device_wonder_mv")
        self.assertEqual(buttons[1].id, "select_device_tzt")
        self.assertEqual(buttons[0].id, "select_device_embed_fire")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_latest_version(self, mock_set_background, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(name=screen.name, key="version", value="v24.07.0")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
            ):
                calls.append(call(wid=button.id, rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_older_version(self, mock_set_background, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(name=screen.name, key="version", value="v24.03.0")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
            ):
                calls.append(call(wid=button.id, rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_with_beta_version(self, mock_set_background, mock_get_locale):
        screen = SelectDeviceScreen()
        self.render(screen)
        screen.update(name=screen.name, key="version", value="odudex/krux_binaries")

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
                "select_device_cube",
            ):
                calls.append(call(wid=button.id, rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_with_latest_version(
        self, mock_set_screen, mock_manager, mock_get_locale
    ):
        mock_manager.get_screen = MagicMock()
        screen = SelectDeviceScreen()
        screen.update(name=screen.name, key="version", value="v24.03.0")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_manager = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_release_{button.id}")
            action(button)

            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 1)))
                calls_manager.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_with_beta_version(
        self, mock_set_screen, mock_manager, mock_get_locale
    ):
        mock_manager.get_screen = MagicMock()
        screen = SelectDeviceScreen()
        screen.update(name=screen.name, key="version", value="odudex/krux_binaries")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_manager = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_release_{button.id}")
            action(button)

            if button.id in (
                "select_device_m5stickv",
                "select_device_amigo",
                "select_device_dock",
                "select_device_bit",
                "select_device_yahboom",
                "select_device_cube",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 1)))
                calls_manager.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_with_v22_03_0_version(
        self, mock_set_screen, mock_manager, mock_get_locale
    ):
        mock_manager.get_screen = MagicMock()
        screen = SelectDeviceScreen()
        screen.update(name=screen.name, key="version", value="v22.03.0")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_manager = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_release_{button.id}")
            action(button)

            if button.id in ("select_device_m5stickv"):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 1)))
                calls_manager.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_locale.assert_called_once()

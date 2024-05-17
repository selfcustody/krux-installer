from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.main_screen import MainScreen


class TestMainScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_main_screen(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "MainScreen")
        self.assertEqual(screen.id, "main_screen")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_grid_layout(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "main_screen_grid")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_render_buttons(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 6)
        self.assertEqual(buttons[5].id, "main_select_version")
        self.assertEqual(buttons[4].id, "main_select_device")
        self.assertEqual(buttons[3].id, "main_flash")
        self.assertEqual(buttons[2].id, "main_wipe")
        self.assertEqual(buttons[1].id, "main_settings")
        self.assertEqual(buttons[0].id, "main_about")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_on_press_cant_flash_or_wipe(
        self, mock_get_running_app, mock_set_background
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []
        for button in grid.children:
            action = getattr(screen, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "main_select_device",
                "main_select_version",
                "main_settings",
                "main_about",
            ):
                calls.append(call(wid=button.id, rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_on_release_cant_flash_or_wipe(
        self, mock_get_running_app, mock_manager, mock_set_screen, mock_set_background
    ):
        mock_manager.get_screen = MagicMock()

        mock_get_running_app.return_value = MagicMock(open_settings=MagicMock())
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_set_screen = []
        calls_manager = []

        for button in grid.children:
            action = getattr(screen, f"on_release_{button.id}")
            action(button)

            if button.id in (
                "main_select_device",
                "main_select_version",
                "main_settings",
                "main_about",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 0)))

            if button.id == "main_select_device":
                calls_set_screen.append(
                    call(name="SelectDeviceScreen", direction="left")
                )
                calls_manager.append(call("SelectDeviceScreen"))

            if button.id == "main_select_version":
                calls_set_screen.append(
                    call(name="SelectVersionScreen", direction="left")
                )
                calls_manager.append(call("SelectVersionScreen"))
                calls_manager.append(call().clear())
                calls_manager.append(call().fetch_releases())
            if button.id == "main_about":
                calls_set_screen.append(call(name="AboutScreen", direction="left"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_get_running_app.assert_has_calls(
            [
                call().config.get("locale", "lang"),
                call().open_settings(),
            ],
            any_order=True,
        )

        mock_get_running_app.return_value.open_settings.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_version(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[5]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(device_button.text, "Version: [color=#00AABB]v24.03.0[/color]")
        self.assertEqual(flash_button.text, "[color=#333333]Flash[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)

        for version in (
            "odudex/krux_binaries",
            "v23.09.1",
            "v23.09.0",
            "v22.08.2",
            "v22.08.1",
            "v22.08.0",
            "v22.03.0",
        ):
            screen.update(name="SelectVersionScreen", key="version", value=version)
            self.assertEqual(
                device_button.text, f"Version: [color=#00AABB]{version}[/color]"
            )
            self.assertEqual(flash_button.text, "[color=#333333]Flash[/color]")
            self.assertEqual(wipe_button.text, "[color=#333333]Wipe[/color]")
            self.assertTrue(flash_button.markup)
            self.assertTrue(wipe_button.markup)

        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_device(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]select a new one[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Flash[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectVersionScreen", key="device", value=device)
            self.assertEqual(
                device_button.text, f"Device: [color=#00AABB]{device}[/color]"
            )
            self.assertEqual(flash_button.text, "Flash")
            self.assertEqual(wipe_button.text, "Wipe")
            self.assertFalse(flash_button.markup)
            self.assertFalse(wipe_button.markup)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_fail_update_invalid_screen(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="MockedScreen", key="device", value="v24.03.0")

        self.assertEqual(str(exc_info.exception), "Invalid screen name: MockedScreen")
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_fail_update_invalid_key(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="SelectDeviceScreen", key="mock", value="mock")

        self.assertEqual(str(exc_info.exception), 'Invalid key: "mock"')
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_update_no_valid_device_but_valid_situation(self, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]select a new one[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Flash[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)

        screen.update(name="SelectDeviceScreen", key="device", value="Mocked device")

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]Mocked device[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Flash[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_on_press_can_flash_or_wipe(
        self, mock_get_running_app, mock_set_background
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        calls = []

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectVersionScreen", key="device", value=device)
            flash_action = getattr(screen, "on_press_main_flash")
            wipe_action = getattr(screen, "on_press_main_wipe")
            flash_action(flash_button)
            wipe_action(wipe_button)
            calls.append(call(wid="main_flash", rgba=(0.5, 0.5, 0.5, 0.5)))
            calls.append(call(wid="main_wipe", rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_on_release_can_flash_or_wipe(
        self, mock_get_running_app, mock_set_screen, mock_set_background
    ):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        calls_set_background = []
        calls_set_screen = []

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectVersionScreen", key="device", value=device)
            flash_action = getattr(screen, "on_release_main_flash")
            wipe_action = getattr(screen, "on_release_main_wipe")
            flash_action(flash_button)
            wipe_action(wipe_button)

            calls_set_background.append(call(wid="main_flash", rgba=(0, 0, 0, 0)))
            calls_set_background.append(call(wid="main_wipe", rgba=(0, 0, 0, 0)))
            calls_set_screen.append(call(name="FlashScreen", direction="left"))
            calls_set_screen.append(call(name="WipeScreen", direction="left"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_running_app.assert_called_once()

from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.main_screen import MainScreen


class TestMainScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "MainScreen")
        self.assertEqual(screen.id, "main_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_grid_layout(self):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "main_screen_grid")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_buttons(self):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 6)
        self.assertEqual(buttons[5].id, "main_select_device")
        self.assertEqual(buttons[4].id, "main_select_version")
        self.assertEqual(buttons[3].id, "main_flash")
        self.assertEqual(buttons[2].id, "main_wipe")
        self.assertEqual(buttons[1].id, "main_settings")
        self.assertEqual(buttons[0].id, "main_about")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_on_press_cant_flash_or_wipe(self, mock_set_background):
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
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_set_screen = []

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

            if button.id == "main_select_version":
                calls_set_screen.append(
                    call(name="SelectVersionScreen", direction="left")
                )

            if button.id == "main_about":
                calls_set_screen.append(call(name="AboutScreen", direction="left"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_manager.get_screen.assert_called_once_with("SelectVersionScreen")
        mock_get_running_app.assert_called_once()
        mock_get_running_app.return_value.open_settings.assert_called_once()

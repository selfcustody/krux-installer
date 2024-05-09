from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.select_version_screen import SelectVersionScreen

MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v24.03.0"},
    {"author": "test", "tag_name": "v23.08.1"},
    {"author": "test", "tag_name": "v23.08.0"},
    {"author": "test", "tag_name": "v22.08.1"},
    {"author": "test", "tag_name": "v22.08.0"},
    {"author": "test", "tag_name": "v22.02.0"},
]


class TestSelectVersionScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = SelectVersionScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectVersionScreen")
        self.assertEqual(screen.id, "select_version_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_grid_layout(self):
        screen = SelectVersionScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_version_screen_grid")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("kivy.uix.gridlayout.GridLayout.clear_widgets")
    def test_clear_grid(self, mock_clear_widgets):
        screen = SelectVersionScreen()
        screen.clear()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_clear_widgets.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    def test_render_buttons(self, mock_manager, mock_requests):
        # Configure mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response
        mock_manager.get_screen = MagicMock()

        screen = SelectVersionScreen()
        screen.fetch_releases()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 4)
        self.assertEqual(buttons[3].id, "select_version_latest")
        self.assertEqual(buttons[2].id, "select_version_beta")
        self.assertEqual(buttons[1].id, "select_version_old")
        self.assertEqual(buttons[0].id, "select_version_back")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    def test_on_press(self, mock_set_background, mock_manager, mock_requests):
        # Configure mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response
        mock_manager.get_screen = MagicMock()

        screen = SelectVersionScreen()
        screen.fetch_releases()
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
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_screen")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    def test_on_release(
        self, mock_manager, mock_set_screen, mock_set_background, mock_requests
    ):
        # Configure mocks
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response
        mock_manager.get_screen = MagicMock()

        screen = SelectVersionScreen()
        screen.fetch_releases()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_set_screen = []
        calls_get_screen = []

        for button in grid.children:
            action = getattr(screen, f"on_release_{button.id}")
            action(button)
            if button.id in (
                "select_version_stable",
                "select_version_beta",
                "select_version_old",
                "select_version_back",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 0)))

            if button.id in ("select_version_stable", "select_version_beta"):
                calls_get_screen.append(call("MainScreen"))
                calls_set_screen.append(call(name="MainScreen", direction="right"))

            if button.id == "select_version_old":
                calls_set_screen.append(
                    call(name="SelectOldVersionScreen", direction="left")
                )

            if button.id == "select_version_back":
                calls_set_screen.append(call(name="MainScreen", direction="right"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_manager.get_screen.assert_has_calls(calls_get_screen)
        mock_set_screen.assert_has_calls(calls_set_screen)

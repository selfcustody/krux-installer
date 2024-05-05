import re
from unittest.mock import patch, MagicMock
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
    def test_on_press_stable(self, mock_set_background, mock_manager, mock_requests):
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
        button = grid.children[3]

        self.assertTrue(re.match(r"^v\d+\.\d+\.\d$", button.text))
        screen.on_press_stable(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_latest", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_screen")
    def test_on_release_stable(
        self, mock_set_screen, mock_set_background, mock_manager, mock_requests
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
        button = grid.children[3]

        self.assertTrue(re.match(r"^v\d+\.\d+\.\d$", button.text))
        screen.on_release_stable(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_latest", rgba=(0, 0, 0, 0)
        )
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    def test_on_press_beta(self, mock_set_background, mock_manager, mock_requests):
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
        button = grid.children[2]

        self.assertEqual(button.text, "odudex/krux_binaries")
        screen.on_press_beta(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_beta", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_screen")
    def test_on_release_beta(
        self, mock_set_screen, mock_set_background, mock_manager, mock_requests
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
        button = grid.children[2]

        self.assertEqual(button.text, "odudex/krux_binaries")
        screen.on_release_beta(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_beta", rgba=(0, 0, 0, 0)
        )
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    def test_on_press_old(self, mock_set_background, mock_manager, mock_requests):
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
        button = grid.children[1]

        self.assertEqual(button.text, "Old versions")
        screen.on_press_old(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_old", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_screen")
    def test_on_release_old(
        self, mock_set_screen, mock_set_background, mock_manager, mock_requests
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
        button = grid.children[1]

        self.assertEqual(button.text, "Old versions")
        screen.on_release_old(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_old", rgba=(0, 0, 0, 0)
        )
        mock_set_screen.assert_called_once_with(
            name="SelectOldVersionScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    def test_on_press_back(self, mock_set_background, mock_manager, mock_requests):
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
        button = grid.children[0]

        self.assertEqual(button.text, "Back")
        screen.on_press_back(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_back", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.utils.selector.requests")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.manager")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_background")
    @patch("src.app.screens.select_version_screen.SelectVersionScreen.set_screen")
    def test_on_release_back(
        self, mock_set_screen, mock_set_background, mock_manager, mock_requests
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
        button = grid.children[0]

        self.assertEqual(button.text, "Back")
        screen.on_release_back(button)
        mock_set_background.assert_called_once_with(
            wid="select_version_back", rgba=(0, 0, 0, 0)
        )
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

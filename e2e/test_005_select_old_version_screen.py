from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.select_old_version_screen import SelectOldVersionScreen

MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v23.08.1"},
    {"author": "test", "tag_name": "v23.08.0"},
    {"author": "test", "tag_name": "v22.08.1"},
    {"author": "test", "tag_name": "v22.08.0"},
    {"author": "test", "tag_name": "v22.02.0"},
]

OLD_VERSIONS = [d["tag_name"] for d in MOCKED_FOUND_API]


class TestSelectVersionScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = SelectOldVersionScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectOldVersionScreen")
        self.assertEqual(screen.id, "select_old_version_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_grid_layout(self):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_old_version_screen_grid")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("kivy.uix.gridlayout.GridLayout.clear_widgets")
    def test_clear_grid(self, mock_clear_widgets):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_clear_widgets.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_register_button_methods(self):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.register_button_methods(name="mock")

        # pylint: disable=no-member
        self.assertTrue(screen.on_press_mock is not None)

        # pylint: disable=no-member
        self.assertTrue(screen.on_release_mock is not None)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_fetch_releases_made_on_press_method(self):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        print(screen.ids["select_old_version_screen_grid"].ids)
        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        for tag in OLD_VERSIONS:
            sanitized = tag.replace(".", "_").replace("/", "_")
            on_press_method = getattr(screen, f"on_press_{sanitized}")
            self.assertTrue(on_press_method is not None)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_fetch_releases_made_on_release_method(self):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        print(screen.ids["select_old_version_screen_grid"].ids)
        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        for tag in OLD_VERSIONS:
            sanitized = tag.replace(".", "_").replace("/", "_")
            on_release_method = getattr(screen, f"on_release_{sanitized}")
            self.assertTrue(on_release_method is not None)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_fetch_releases_made_button(self):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        print(screen.ids["select_old_version_screen_grid"].ids)
        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        for tag in OLD_VERSIONS:
            sanitized = tag.replace(".", "_").replace("/", "_")
            self.assertTrue(f"select_old_version_{sanitized}" in screen.ids)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_background"
    )
    def test_on_press(self, mock_set_background):
        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        calls = []
        for tag in OLD_VERSIONS:
            sanitized = tag.replace(".", "_").replace("/", "_")
            button = screen.ids[f"select_old_version_{sanitized}"]
            on_press = getattr(screen, f"on_press_{sanitized}")
            on_press(button)
            calls.append(
                call(wid=f"select_old_version_{sanitized}", rgba=(0.5, 0.5, 0.5, 0.5))
            )

        back_button = screen.ids["select_old_version_back"]
        screen.on_press_back(back_button)
        calls.append(call(wid="select_old_version_back", rgba=(0.5, 0.5, 0.5, 0.5)))

        mock_set_background.assert_has_calls(calls)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_old_version_screen.SelectOldVersionScreen.manager")
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_background"
    )
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_screen"
    )
    def test_on_release(self, mock_set_screen, mock_set_background, mock_manager):
        mock_manager.get_screen = MagicMock()

        screen = SelectOldVersionScreen()
        screen.make_grid_if_not_exist(OLD_VERSIONS)
        screen.clear()
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        set_background_calls = []
        set_screen_calls = []
        for tag in OLD_VERSIONS:
            sanitized = tag.replace(".", "_").replace("/", "_")
            button = screen.ids[f"select_old_version_{sanitized}"]
            on_release = getattr(screen, f"on_release_{sanitized}")
            on_release(button)
            set_background_calls.append(
                call(wid=f"select_old_version_{sanitized}", rgba=(0, 0, 0, 0))
            )
            set_screen_calls.append(call(name="MainScreen", direction="right"))

        back_button = screen.ids["select_old_version_back"]
        screen.on_release_back(back_button)
        set_background_calls.append(
            call(wid="select_old_version_back", rgba=(0, 0, 0, 0))
        )
        set_screen_calls.append(call(name="SelectVersionScreen", direction="right"))

        mock_set_background.assert_has_calls(set_background_calls)
        mock_set_screen.assert_has_calls(set_screen_calls)

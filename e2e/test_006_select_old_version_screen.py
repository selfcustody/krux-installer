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


class TestSelectOldVersionScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = SelectOldVersionScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectOldVersionScreen")
        self.assertEqual(screen.id, "select_old_version_screen")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_grid_layout(self, mock_get_locale):
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.get = MagicMock(return_value="en-US")

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_old_version_screen_grid")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("kivy.uix.gridlayout.GridLayout.clear_widgets")
    def test_clear_grid(self, mock_clear_widgets, mock_get_locale):
        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_clear_widgets.assert_called_once()
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_background"
    )
    def test_on_press(self, mock_set_background, mock_get_locale):
        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        calls = []
        for button in grid.children:
            on_press = getattr(screen, f"on_press_{button.id}")
            on_press(button)
            calls.append(call(wid=button.id, rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.select_old_version_screen.SelectOldVersionScreen.manager")
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_background"
    )
    @patch(
        "src.app.screens.select_old_version_screen.SelectOldVersionScreen.set_screen"
    )
    def test_on_release(
        self, mock_set_screen, mock_set_background, mock_manager, mock_get_locale
    ):
        mock_manager.get_screen = MagicMock()

        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(len(grid.children), len(OLD_VERSIONS) + 1)

        set_background_calls = []
        set_screen_calls = []

        for button in grid.children:
            on_release = getattr(screen, f"on_release_{button.id}")
            on_release(button)
            set_background_calls.append(call(wid=button.id, rgba=(0, 0, 0, 1)))

            if button.id == "select_old_version_back":
                set_screen_calls.append(
                    call(name="SelectVersionScreen", direction="right")
                )
            else:
                set_screen_calls.append(call(name="MainScreen", direction="right"))

        mock_set_background.assert_has_calls(set_background_calls)
        mock_set_screen.assert_has_calls(set_screen_calls)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_locale(self, mock_redirect_exception, mock_get_locale):
        screen = SelectOldVersionScreen()
        screen.make_grid(
            wid="select_old_version_screen_grid", rows=len(OLD_VERSIONS) + 1
        )
        screen.clear_grid(wid="select_old_version_screen_grid")
        screen.fetch_releases(OLD_VERSIONS)
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name="Mock", key="locale", value="pt_BR.UTF-8")

        mock_get_locale.assert_any_call()
        mock_redirect_exception.assert_called_once()

from unittest.mock import patch, MagicMock
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
    def test_on_press_select_device(self, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        screen.on_press_select_device(button)
        mock_set_background.assert_called_once_with(
            wid="main_select_device", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_on_release_select_device(self, mock_set_screen, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        screen.on_release_select_device(button)
        mock_set_background.assert_called_once_with(
            wid="main_select_device", rgba=(0, 0, 0, 0)
        )
        mock_set_screen.assert_called_once_with(
            name="SelectDeviceScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_on_press_select_version(self, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[1]

        screen.on_press_select_version(button)
        mock_set_background.assert_called_once_with(
            wid="main_select_version", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_on_release_select_version(
        self, mock_set_screen, mock_set_background, mock_manager
    ):
        mock_manager.get_screen = MagicMock()
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[1]

        screen.on_release_select_version(button)
        mock_set_background.assert_called_once_with(
            wid="main_select_version", rgba=(0, 0, 0, 0)
        )
        mock_set_screen.assert_called_once_with(
            name="SelectVersionScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_fail_on_press_flash(self, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        screen.on_press_flash(button)
        self.assertEqual(len(mock_set_background.call_args_list), 0)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_on_press_flash(self, mock_set_background):
        screen = MainScreen()
        screen.will_flash = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        screen.on_press_flash(button)
        mock_set_background.assert_called_once_with(
            wid="main_flash", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_fail_on_release_flash(self, mock_set_screen, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        screen.on_release_flash(button)
        self.assertEqual(len(mock_set_background.call_args_list), 0)
        self.assertEqual(len(mock_set_screen.call_args_list), 0)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_on_release_flash(self, mock_set_screen, mock_set_background):
        screen = MainScreen()
        screen.will_flash = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        screen.on_release_flash(button)
        mock_set_background.assert_called_once_with(wid="main_flash", rgba=(0, 0, 0, 0))
        mock_set_screen.assert_called_once_with(name="FlashScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_fail_on_press_wipe(self, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        screen.on_press_wipe(button)
        self.assertEqual(len(mock_set_background.call_args_list), 0)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_on_press_wipe(self, mock_set_background):
        screen = MainScreen()
        screen.will_wipe = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        screen.on_press_wipe(button)
        mock_set_background.assert_called_once_with(
            wid="main_wipe", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_fail_on_release_wipe(self, mock_set_screen, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        screen.on_release_wipe(button)
        self.assertEqual(len(mock_set_background.call_args_list), 0)
        self.assertEqual(len(mock_set_screen.call_args_list), 0)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_on_release_wipe(self, mock_set_screen, mock_set_background):
        screen = MainScreen()
        screen.will_wipe = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        screen.on_release_wipe(button)
        mock_set_background.assert_called_once_with(wid="main_wipe", rgba=(0, 0, 0, 0))
        mock_set_screen.assert_called_once_with(name="WipeScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_on_press_settings(self, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[4]

        screen.on_press_settings(button)
        mock_set_background.assert_called_once_with(
            wid="main_settings", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.App.get_running_app")
    def test_on_release_settings(self, mock_get_running_app, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[4]

        screen.on_release_settings(button)
        mock_set_background.assert_called_once_with(
            wid="main_settings", rgba=(0, 0, 0, 0)
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    def test_on_press_about(self, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[5]

        screen.on_press_about(button)
        mock_set_background.assert_called_once_with(
            wid="main_about", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    def test_on_release_about(self, mock_set_screen, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        screen.on_release_about(button)
        mock_set_background.assert_called_once_with(wid="main_about", rgba=(0, 0, 0, 0))
        mock_set_screen.assert_called_once_with(name="AboutScreen", direction="left")

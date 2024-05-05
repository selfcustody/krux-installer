from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.select_device_screen import SelectDeviceScreen


class TestSelectDeviceScreen(GraphicUnitTest):

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_main_screen(self):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "SelectDeviceScreen")
        self.assertEqual(screen.id, "select_device_screen")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_grid_layout(self):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "select_device_screen_grid")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    def test_render_buttons(self):
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

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_m5stickv(self, mock_set_background):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[5]

        self.assertEqual(button.text, "m5stickv")
        screen.on_press_m5stickv(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_m5stickv", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_m5stickv(
        self, mock_set_screen, mock_manager, mock_set_background
    ):
        mock_manager.get_screen = MagicMock()

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[5]

        self.assertEqual(button.text, "m5stickv")
        screen.on_release_m5stickv(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_m5stickv", rgba=(0, 0, 0, 0)
        )
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_amigo(self, mock_set_background):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[4]

        self.assertEqual(button.text, "amigo")
        screen.on_press_amigo(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_amigo", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_amigo(self, mock_set_screen, mock_manager, mock_set_background):
        mock_manager.get_screen = MagicMock()

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[4]

        self.assertEqual(button.text, "amigo")
        screen.on_release_amigo(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_amigo", rgba=(0, 0, 0, 0)
        )
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_dock(self, mock_set_background):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        self.assertEqual(button.text, "dock")
        screen.on_press_dock(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_dock", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_dock(self, mock_set_screen, mock_manager, mock_set_background):
        mock_manager.get_screen = MagicMock()

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        self.assertEqual(button.text, "dock")
        screen.on_release_dock(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_dock", rgba=(0, 0, 0, 0)
        )
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_bit(self, mock_set_background):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        self.assertEqual(button.text, "bit")
        screen.on_press_bit(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_bit", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_bit(self, mock_set_screen, mock_manager, mock_set_background):
        mock_manager.get_screen = MagicMock()

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        self.assertEqual(button.text, "bit")
        screen.on_release_bit(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_bit", rgba=(0, 0, 0, 0)
        )
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_yahboom(self, mock_set_background):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[1]

        self.assertEqual(button.text, "yahboom")
        screen.on_press_yahboom(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_yahboom", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_yahboom(
        self, mock_set_screen, mock_manager, mock_set_background
    ):
        mock_manager.get_screen = MagicMock()

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[1]

        self.assertEqual(button.text, "yahboom")
        screen.on_release_yahboom(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_yahboom", rgba=(0, 0, 0, 0)
        )
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    def test_on_press_cube(self, mock_set_background):
        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        self.assertEqual(button.text, "cube")
        screen.on_press_cube(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_cube", rgba=(0.5, 0.5, 0.5, 0.5)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_background")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.manager")
    @patch("src.app.screens.select_device_screen.SelectDeviceScreen.set_screen")
    def test_on_release_cube(self, mock_set_screen, mock_manager, mock_set_background):
        mock_manager.get_screen = MagicMock()

        screen = SelectDeviceScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        self.assertEqual(button.text, "cube")
        screen.on_release_cube(button)
        mock_set_background.assert_called_once_with(
            wid="select_device_cube", rgba=(0, 0, 0, 0)
        )
        mock_manager.get_screen.assert_called_once_with("MainScreen")
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

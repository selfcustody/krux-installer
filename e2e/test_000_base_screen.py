import os
from pathlib import Path
from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager
from src.app.screens.base_screen import BaseScreen


class TestBaseScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch("sys.platform", "linux")
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_static_get_locale_linux(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.config = MagicMock()
        mock_get_ruunning_app.return_value.config.get = MagicMock()
        mock_get_ruunning_app.return_value.config.get.side_effect = ["en-US.UTF-8"]

        # your asserts
        self.assertEqual(BaseScreen.get_locale(), "en_US.UTF-8")

    @patch("sys.platform", "darwin")
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_static_get_locale_darwin(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.config = MagicMock()
        mock_get_ruunning_app.return_value.config.get = MagicMock()
        mock_get_ruunning_app.return_value.config.get.side_effect = ["en-US.UTF-8"]

        # your asserts
        self.assertEqual(BaseScreen.get_locale(), "en_US.UTF-8")

    @patch("sys.platform", "win32")
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_static_get_locale_win32(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.config = MagicMock()
        mock_get_ruunning_app.return_value.config.get = MagicMock()
        mock_get_ruunning_app.return_value.config.get.side_effect = ["en_US"]

        # your asserts
        self.assertEqual(BaseScreen.get_locale(), "en_US.UTF-8")

    @patch("sys.platform", "mockos")
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_get_locale(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.config = MagicMock()
        mock_get_ruunning_app.return_value.config.get = MagicMock()
        mock_get_ruunning_app.return_value.config.get.side_effect = ["en_US"]

        with self.assertRaises(RuntimeError) as exc_info:
            BaseScreen.get_locale()

        self.assertEqual(str(exc_info.exception), "Not implemented for 'mockos'")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_static_get_destdir_assets(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.config = MagicMock()
        mock_get_ruunning_app.return_value.config.get = MagicMock()
        mock_get_ruunning_app.return_value.config.get.side_effect = [
            os.path.join("tmp", "mock")
        ]

        # your asserts
        self.assertEqual(BaseScreen.get_destdir_assets(), os.path.join("tmp", "mock"))

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_static_get_baudrate(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.config = MagicMock()
        mock_get_ruunning_app.return_value.config.get = MagicMock()
        mock_get_ruunning_app.return_value.config.get.side_effect = [15000000]

        # your asserts
        self.assertEqual(BaseScreen.get_baudrate(), 15000000)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_static_open_settings(self, mock_get_ruunning_app):
        mock_get_ruunning_app.return_value = MagicMock()
        mock_get_ruunning_app.return_value.open_settings = MagicMock()

        BaseScreen.open_settings()
        mock_get_ruunning_app.return_value.open_settings.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init_linux(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(window.children[0].height, window.height)

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_init_win32(self, mock_get_locale):

        screen = BaseScreen(wid="mock", name="Mock")
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # your asserts
        self.assertEqual(window.children[0], screen)
        self.assertEqual(window.children[0].height, window.height)

        mock_get_locale.assert_called_once()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_get_logo_img(self, mock_get_locale):
        root = Path(__file__).parent.parent
        logo = os.path.join(root, "assets", "logo.png")
        screen = BaseScreen(wid="mock", name="Mock")
        self.assertEqual(screen.logo_img, logo)

        mock_get_locale.assert_called_once()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_get_warn_img(self, mock_get_locale):
        root = Path(__file__).parent.parent
        warn = os.path.join(root, "assets", "warning.png")
        screen = BaseScreen(wid="mock", name="Mock")
        self.assertEqual(screen.warn_img, warn)

        mock_get_locale.assert_called_once()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_get_load_gif(self, mock_get_locale):
        root = Path(__file__).parent.parent
        warn = os.path.join(root, "assets", "load.gif")
        screen = BaseScreen(wid="mock", name="Mock")
        self.assertEqual(screen.load_img, warn)

        mock_get_locale.assert_called_once()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_get_done_img(self, mock_get_locale):
        root = Path(__file__).parent.parent
        warn = os.path.join(root, "assets", "done.png")
        screen = BaseScreen(wid="mock", name="Mock")
        self.assertEqual(screen.done_img, warn)

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_set_background(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.ids = {}
        screen.ids["mocked_button"] = Button()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        screen.set_background(wid="mocked_button", rgba=(0, 0, 0, 0))

        # your asserts
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[0], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[1], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[2], 0)
        self.assertEqual(window.children[0].ids["mocked_button"].background_color[3], 0)

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_set_screen(self, mock_get_locale):
        screen_manager = ScreenManager()
        screen_0 = BaseScreen(wid="mock_0", name="Mock_0")
        screen_1 = BaseScreen(wid="mock_1", name="Mock_1")

        screen_manager.add_widget(screen_0)
        screen_manager.add_widget(screen_1)
        self.render(screen_manager)

        self.assertEqual(screen_manager.current, "Mock_0")

        screen_0.set_screen(name="Mock_1", direction="left")
        self.assertEqual(screen_manager.current, "Mock_1")

        screen_1.set_screen(name="Mock_0", direction="right")
        self.assertEqual(screen_manager.current, "Mock_0")

        mock_get_locale.assert_has_calls([call(), call()], any_order=True)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_make_grid(self, mock_get_locale):
        screen_0 = BaseScreen(wid="mock", name="Mock")
        screen_0.make_grid(wid="mock_grid", rows=1)
        self.render(screen_0)

        EventLoop.ensure_window()
        window = EventLoop.window
        screen = window.children[0]

        self.assertTrue("mock_grid" in screen.ids)
        self.assertEqual(screen.id, "mock")
        self.assertEqual(screen.name, "Mock")

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_make_subgrid(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.make_grid(wid="mock_grid", rows=1)
        screen.make_subgrid(wid="mock_subgrid", rows=1, root_widget="mock_grid")
        self.render(screen)

        EventLoop.ensure_window()

        self.assertTrue("mock_grid" in screen.ids)
        self.assertTrue("mock_subgrid" in screen.ids)
        self.assertEqual(screen.id, "mock")
        self.assertEqual(screen.name, "Mock")

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_make_label(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.make_grid(wid="mock_grid", rows=1)
        screen.make_label(
            wid="mock_label",
            root_widget="mock_grid",
            halign="center",
            text="mock",
        )
        self.render(screen)

        EventLoop.ensure_window()

        self.assertTrue("mock_grid" in screen.ids)
        self.assertTrue("mock_label" in screen.ids)
        self.assertEqual(screen.ids["mock_label"].text, "mock")
        self.assertEqual(screen.id, "mock")
        self.assertEqual(screen.name, "Mock")

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_make_button(self, mock_get_locale):
        screen_0 = BaseScreen(wid="mock", name="Mock")
        screen_0.make_grid(wid="mock_grid", rows=1)
        screen_0.make_button(
            row=0,
            wid="mock_button",
            root_widget="mock_grid",
            text="Mocked button",
            on_press=MagicMock(),
            on_release=MagicMock(),
        )
        self.render(screen_0)

        EventLoop.ensure_window()
        window = EventLoop.window
        screen = window.children[0]

        self.assertTrue("mock_button" in screen.ids)

        button = screen.ids["mock_button"]

        # pylint: disable=protected-access
        button._do_press()
        button.dispatch("on_press")

        # pylint: disable=protected-access
        button._do_release()
        button.dispatch("on_release")

        screen.on_press_mock_button.assert_called_once()
        screen.on_release_mock_button.assert_called_once()

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    def test_clear_grid(self, mock_get_locale):
        screen_0 = BaseScreen(wid="mock", name="Mock")
        screen_0.make_grid(wid="mock_grid", rows=3)

        for i in range(0, 2):
            screen_0.make_button(
                row=i,
                wid=f"mock_button_{i}",
                root_widget="mock_grid",
                text="Mocked button",
                on_press=MagicMock(),
                on_release=MagicMock(),
            )
        self.render(screen_0)

        EventLoop.ensure_window()
        window = EventLoop.window
        screen = window.children[0]
        grid = screen.children[0]

        screen.clear_grid(wid="mock_grid")
        self.assertFalse("mock_button_0" in grid.ids)

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_screen_invalid_screen(
        self, mock_redirect_exception, mock_get_locale
    ):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.make_grid(wid="mock_grid", rows=1)
        screen.make_button(
            row=0,
            wid="mock_button",
            root_widget="mock_grid",
            text="Mocked button",
            on_press=MagicMock(),
            on_release=MagicMock(),
        )
        self.render(screen)
        screen.update_screen(
            name="NoMockedScreen",
            key="",
            value="",
            allowed_screens=("MockedScreen",),
            on_update=MagicMock(),
        )
        mock_get_locale.assert_called_once()
        mock_redirect_exception.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_screen_locale(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.make_grid(wid="mock_grid", rows=1)
        screen.make_button(
            row=0,
            wid="mock_button",
            root_widget="mock_grid",
            text="Mocked button",
            on_press=MagicMock(),
            on_release=MagicMock(),
        )
        self.render(screen)
        self.assertEqual(screen.locale, "en_US.UTF-8")

        screen.update_screen(
            name="MockedScreen",
            key="locale",
            value="mocked",
            allowed_screens=("MockedScreen",),
            on_update=MagicMock(),
        )
        self.assertEqual(screen.locale, "mocked")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.BaseScreen.get_locale")
    @patch("src.app.screens.base_screen.Color")
    @patch("src.app.screens.base_screen.Rectangle")
    def test_update_screen_canvas(self, mock_rectangle, mock_color, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.make_grid(wid="mock_grid", rows=1)
        screen.make_button(
            row=0,
            wid="mock_button",
            root_widget="mock_grid",
            text="Mocked button",
            on_press=MagicMock(),
            on_release=MagicMock(),
        )
        self.render(screen)
        screen.update_screen(
            name="MockedScreen",
            key="canvas",
            value="",
            allowed_screens=("MockedScreen",),
            on_update=MagicMock(),
        )

        mock_color.assert_called_once_with(0, 0, 0, 1)
        mock_rectangle.assert_called_once()
        mock_get_locale.assert_called_once()

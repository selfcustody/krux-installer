import os
from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.warning_wipe_screen import WarningWipeScreen


class TestWarningWipeScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        noto_sans_path = os.path.join(assets_path, "NotoSansCJK_Cy_SC_KR_Krux.ttf")
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.warning_wipe_screen.partial")
    @patch("src.app.screens.warning_wipe_screen.Clock.schedule_once")
    def test_init(self, mock_schedule_once, mock_partial, mock_get_locale):
        screen = WarningWipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        image = grid.children[1]
        label = grid.children[0]

        # default assertions
        self.assertEqual(grid.id, "warning_wipe_screen_grid")
        self.assertEqual(len(grid.children), 2)
        self.assertEqual(image.id, "warning_wipe_screen_warn")
        self.assertEqual(label.id, "warning_wipe_screen_label")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_partial.assert_called_once_with(
            screen.update, name=screen.name, key="canvas"
        )
        mock_schedule_once.assert_has_calls([call(mock_partial(), 0)], any_order=True)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_make_label_text(self, mock_get_locale):
        screen = WarningWipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        label = grid.children[0]
        screen.update(name=screen.name, key="locale", value="en_US.UTF-8")

        text = "".join(
            [
                "[color=#EFCC00]",
                "You are about to initiate a FULL WIPE of this device",
                "[/color]",
                "\n",
                "\n",
                "This operation will:",
                "\n",
                "* Permanently erase all saved data",
                "\n",
                "* Remove the existing firmware",
                "\n",
                "* Render the device non-functional until new firmware is re-flashed",
                "\n",
                "\n",
                "[color=#00FF00]",
                "[ref=WipeScreen][u]Proceed[/u][/ref]",
                "[/color]",
                "        ",
                "[color=#FF0000]",
                "[ref=MainScreen][u]Back[/u][/ref]",
                "[/color]",
            ]
        )

        self.assertEqual(label.text, text)

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.warning_wipe_screen.WarningWipeScreen.make_label_text",
        return_value="mocked",
    )
    def test_update_locale(self, mock_make_label_text, mock_get_locale):
        screen = WarningWipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="locale", value="en_US.UTF8")

        self.assertEqual(screen.locale, "en_US.UTF8")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_make_label_text.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.warning_wipe_screen.WarningWipeScreen.make_label_text",
        return_value="mocked",
    )
    def test_on_enter(self, mock_make_label_text, mock_get_locale):
        screen = WarningWipeScreen()
        self.render(screen)
        screen.on_enter()

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_make_label_text.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.get_baudrate", return_value=1500000)
    @patch("src.app.screens.warning_wipe_screen.partial")
    @patch("src.app.screens.warning_wipe_screen.Clock.schedule_once")
    def test_on_ref_press_proceed(
        self, mock_schedule_once, mock_partial, mock_get_baudrate, mock_get_locale
    ):
        screen = WarningWipeScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        label = grid.children[0]
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(label, "WipeScreen")

        mock_get_locale.assert_any_call()
        screen.manager.get_screen.assert_has_calls(
            [call("MainScreen"), call("WipeScreen")]
        )
        mock_get_baudrate.assert_called_once()
        mock_partial.assert_has_calls(
            [
                call(
                    screen.manager.get_screen().update,
                    name=screen.name,
                    key="device",
                    value=screen.manager.get_screen().device,
                ),
                call(
                    screen.manager.get_screen().update,
                    name=screen.name,
                    key="wiper",
                    value=1500000,
                ),
            ],
            any_order=True,
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 0)], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.warning_wipe_screen.WarningWipeScreen.set_screen")
    def test_on_ref_press_deny(self, mock_set_screen, mock_get_locale):
        screen = WarningWipeScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        label = grid.children[0]
        button = screen.ids[f"{screen.id}_label"]
        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(label, "MainScreen")

        mock_get_locale.assert_any_call()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

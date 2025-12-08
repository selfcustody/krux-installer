import os
import sys
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.about_screen import AboutScreen

# Import tomllib for Python 3.11+ or tomli for earlier versions
if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class TestAboutScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        font_name = "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
        noto_sans_path = os.path.join(assets_path, font_name)
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

        # Read version from pyproject.toml
        pyproject_path = os.path.join(cwd_path, "..", "pyproject.toml")
        pyproject_abs_path = os.path.abspath(pyproject_path)
        with open(pyproject_abs_path, "rb") as f:
            pyproject_data = tomllib.load(f)
        cls.version = pyproject_data["project"]["version"]

    @classmethod
    def teardown_class(cls):
        # Unschedule all pending Clock events to prevent race conditions
        # with subsequent tests
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        label = grid.children[0]

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "AboutScreen")
        self.assertEqual(screen.id, "about_screen")
        self.assertEqual(grid.id, "about_screen_grid")
        self.assertEqual(label.id, "about_screen_label")

        text = "".join(
            [
                f"[ref=SourceCode][b]v{self.version}[/b][/ref]",
                "\n",
                "\n",
                "follow us on X: ",
                "[color=#00AABB]",
                "[ref=X][u]@selfcustodykrux[/u][/ref]",
                "[/color]",
                "\n",
                "\n",
                "[color=#00FF00]",
                "[ref=Back]",
                "[u]Back[/u]",
                "[/ref]",
                "[/color]",
            ]
        )

        self.assertEqual(label.text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="pt_BR.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        label = grid.children[0]

        screen.update(name="ConfigKruxInstaller", key="locale", value="pt_BR.UTF-8")

        text = "".join(
            [
                f"[ref=SourceCode][b]v{self.version}[/b][/ref]",
                "\n",
                "\n",
                "siga-nos no X: ",
                "[color=#00AABB]",
                "[ref=X][u]@selfcustodykrux[/u][/ref]",
                "[/color]",
                "\n",
                "\n",
                "[color=#00FF00]",
                "[ref=Back]",
                "[u]Voltar[/u]",
                "[/ref]",
                "[/color]",
            ]
        )
        self.assertEqual(label.text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.about_screen.webbrowser")
    def test_on_press_version(self, mock_webbrowser, mock_get_locale):
        mock_webbrowser.open = MagicMock()

        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action("Mock", "SourceCode")

        mock_get_locale.assert_any_call()
        mock_webbrowser.open.assert_called_once_with(
            "https://selfcustody.github.io/krux/getting-started/installing/from-gui/"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.about_screen.webbrowser")
    def test_on_press_x_formerly_known_as_twitter(
        self, mock_webbrowser, mock_get_locale
    ):
        mock_webbrowser.open = MagicMock()

        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action("Mock", "X")

        mock_get_locale.assert_any_call()
        mock_webbrowser.open.assert_called_once_with("https://x.com/selfcustodykrux")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.about_screen.AboutScreen.set_screen")
    def test_on_press_back(self, mock_set_screen, mock_get_locale):
        screen = AboutScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action("Mock", "Back")

        mock_get_locale.assert_any_call()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")

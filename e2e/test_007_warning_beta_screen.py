import os
import sys
from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.warning_beta_screen import WarningBetaScreen


class TestSelectVersionScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        terminus_path = os.path.join(assets_path, "terminus.ttf")
        nanum_path = os.path.join(assets_path, "NanumGothic-Regular.ttf")
        LabelBase.register(name="terminus", fn_regular=terminus_path)
        LabelBase.register(name="nanum", fn_regular=nanum_path)
        LabelBase.register(DEFAULT_FONT, terminus_path)

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        fontsize_mm = 0
        fontsize_m = 0
        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_mm = window.size[0] // 24
            fontsize_m = window.size[0] // 32
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_mm = window.size[0] // 48
            fontsize_m = window.size[0] // 64
            fontsize_mp = window.size[0] // 128

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WarningBetaScreen")
        self.assertEqual(screen.id, "warning_beta_screen")
        self.assertEqual(grid.id, "warning_beta_screen_grid")
        self.assertEqual(button.id, "warning_beta_screen_warn")

        text = "".join(
            [
                f"[font={WarningBetaScreen.get_font_name()}]",
                f"[size={fontsize_mm}sp][color=#efcc00][b]WARNING[/b][/color][/size]",
                "\n",
                "\n",
                f"[size={fontsize_m}sp][color=#efcc00]This is our test repository[/color][/size]",
                "\n",
                f"[size={fontsize_mp}sp]These are unsigned binaries for the latest and most experimental features[/size]",
                "\n",
                f"[size={fontsize_mp}sp]and it's just for trying new things and providing feedback.[/size]",
                "\n",
                "\n",
                f"[size={fontsize_mm}sp]",
                "[color=#00ff00]Proceed[/color]        [color=#ff0000]Back[/color]",
                "[/size]",
                "[/font]",
            ]
        )

        self.assertEqual(button.text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.warning_beta_screen.WarningBetaScreen.set_background")
    def test_on_press(self, mock_set_background, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_press_warning_beta_screen_warn")
        action(button)

        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.25, 0.25, 0.25, 1)
        )
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.warning_beta_screen.WarningBetaScreen.set_background")
    @patch("src.app.screens.warning_beta_screen.WarningBetaScreen.set_screen")
    def test_on_release(self, mock_set_screen, mock_set_background, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        action = getattr(screen, "on_release_warning_beta_screen_warn")
        action(button)
        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 1))
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[0]

        fontsize_mm = 0
        fontsize_m = 0
        fontsize_mp = 0

        if sys.platform in ("linux", "win32"):
            fontsize_mm = window.size[0] // 24
            fontsize_m = window.size[0] // 32
            fontsize_mp = window.size[0] // 48

        if sys.platform == "darwin":
            fontsize_mm = window.size[0] // 48
            fontsize_m = window.size[0] // 64
            fontsize_mp = window.size[0] // 128

        screen.update(name="ConfigKruxInstaller", key="locale", value="pt_BR.UTF-8")
        text = "".join(
            [
                f"[font={WarningBetaScreen.get_font_name()}]",
                f"[size={fontsize_mm}sp][color=#efcc00][b]ADVERTÊNCIA[/b][/color][/size]",
                "\n",
                "\n",
                f"[size={fontsize_m}sp][color=#efcc00]Este é nosso repositório de testes[/color][/size]",
                "\n",
                f"[size={fontsize_mp}sp]Estes são binários não assinados das últimas e mais experimentais características[/size]",
                "\n",
                f"[size={fontsize_mp}sp]e serve apenas para experimentar coisas novas e fornecer opiniões.[/size]",
                "\n",
                "\n",
                f"[size={fontsize_mm}sp]",
                "[color=#00ff00]Proceder[/color]        [color=#ff0000]Voltar[/color]",
                "[/size]",
                "[/font]",
            ]
        )

        self.assertEqual(button.text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_fail_update_locale_wrong_name(self, mock_redirect_error, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="Mock", key="locale", value="pt_BR.UTF-8")

        mock_redirect_error.assert_called_once_with("Invalid screen name: Mock")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_fail_update_locale_wrong_key(self, mock_redirect_error, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="ConfigKruxInstaller", key="mock")

        mock_redirect_error.assert_called_once_with('Invalid key: "mock"')
        mock_get_locale.assert_any_call()

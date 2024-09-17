import os
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
        noto_sans_path = os.path.join(assets_path, "NotoSansCJK_Cy_SC_KR_Krux.ttf")
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

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
        warn = grid.children[1]
        button = grid.children[0]

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WarningBetaScreen")
        self.assertEqual(screen.id, "warning_beta_screen")
        self.assertEqual(grid.id, "warning_beta_screen_grid")
        self.assertEqual(warn.id, "warning_beta_screen_warn")
        self.assertEqual(button.id, "warning_beta_screen_label")

        text = "".join(
            [
                "[color=#efcc00]This is our test repository[/color]",
                "\n",
                "These are unsigned binaries for the latest and most experimental features",
                "\n",
                "and it's just for trying new things and providing feedback.",
                "\n",
                "\n",
                "[color=#00ff00]",
                "[ref=MainScreen]Proceed[/ref]",
                "[/color]",
                "        ",
                "[color=#ff0000]",
                "[ref=SelectVersion]Back[/ref]",
                "[/color]",
            ]
        )

        self.assertEqual(button.text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_proceed(self, mock_set_screen, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        action = getattr(screen, "on_ref_press_warning_beta_screen_label")
        action("MainScreen")

        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_back(self, mock_set_screen, mock_get_locale):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        action = getattr(screen, "on_ref_press_warning_beta_screen_label")
        action("SelectVersion")

        mock_set_screen.assert_called_once_with(
            name="SelectVersionScreen", direction="right"
        )
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

        screen.update(name="ConfigKruxInstaller", key="locale", value="pt_BR.UTF-8")
        text = "".join(
            [
                "[color=#efcc00]Este é nosso repositório de testes[/color]",
                "\n",
                "Estes são binários não assinados dos recursos mais experimentais",
                "\n",
                "e serve apenas para experimentar coisas novas e dar opiniões.",
                "\n",
                "\n",
                "[color=#00ff00]",
                "[ref=MainScreen]Proceder[/ref]",
                "[/color]",
                "        ",
                "[color=#ff0000]",
                "[ref=SelectVersion]Voltar[/ref]",
                "[/color]",
            ]
        )

        self.assertEqual(button.text, text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_locale_wrong_name(
        self, mock_redirect_exception, mock_get_locale
    ):
        screen = WarningBetaScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="Mock", key="locale", value="pt_BR.UTF-8")

        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_any_call()

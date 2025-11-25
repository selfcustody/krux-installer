import os
from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.warning_after_airgap_update_screen import (
    WarningAfterAirgapUpdateScreen,
)


class TestWarningAfterAirgapUpdateScreen(GraphicUnitTest):

    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        font_name = "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
        noto_sans_path = os.path.join(assets_path, font_name)
        LabelBase.register(DEFAULT_FONT, noto_sans_path)

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
        screen = WarningAfterAirgapUpdateScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WarningAfterAirgapUpdateScreen")
        self.assertEqual(screen.id, "warning_after_airgap_update_screen")
        self.assertTrue("warning_after_airgap_update_screen_grid" in screen.ids)
        self.assertTrue("warning_after_airgap_update_screen_subgrid" in screen.ids)
        self.assertTrue("warning_after_airgap_update_screen_done" in screen.ids)
        self.assertTrue("warning_after_airgap_update_screen_menu" in screen.ids)
        self.assertTrue("warning_after_airgap_update_screen_label" in screen.ids)

        mock_get_locale.assert_called()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.warning_after_airgap_update_screen.WarningAfterAirgapUpdateScreen.quit_app"
    )
    def test_on_ref_press_quit(self, mock_quit_app, mock_get_locale):
        screen = WarningAfterAirgapUpdateScreen()

        action = getattr(screen, "on_ref_press_warning_after_airgap_update_screen_menu")
        action("Quit")

        mock_quit_app.assert_called_once()
        mock_get_locale.assert_any_call()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_back(self, mock_set_screen, mock_get_locale):
        screen = WarningAfterAirgapUpdateScreen()

        action = getattr(screen, "on_ref_press_warning_after_airgap_update_screen_menu")
        action("MainScreen")

        mock_set_screen.assert_called_once_with(name="MainScreen", direction="right")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_update_locale(self, mock_get_locale):
        screen = WarningAfterAirgapUpdateScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="label")
        screen.update(name=screen.name, key="sdcard", value=os.path.join("tmp", "mock"))
        screen.update(name=screen.name, key="hash", value="abcdef01234567890a")
        screen.update(name=screen.name, key="locale", value="en_US.UTF-8")

        text_menu = "".join(
            [
                ".bin and .sig have been copied to",
                "\n",
                f"[color=#efcc00]{os.path.join('tmp', 'mock')}[/color].",
                "\n",
                "\n",
                "[color=#ff0000]",
                "[u][ref=Quit]Quit[/ref][/u]",
                "[/color]",
                "        ",
                "[color=#00ff00]",
                "[u][ref=MainScreen]Back[/ref][/u]",
                "[/color]",
            ]
        )

        text_label = "".join(
            [
                "* Insert the SDcard into your device and reboot it to update.",
                "\n",
                "\n",
                "* You should see this computed hash on device screen:",
                "\n",
                "\n",
                "[color=#efcc00]ab   cd   ef   01   23   45   67   89   0a",
                "[/color]",
            ]
        )

        self.assertEqual(screen.ids[f"{screen.id}_menu"].text, text_menu)
        self.assertEqual(screen.ids[f"{screen.id}_label"].text, text_label)
        mock_get_locale.assert_any_call()

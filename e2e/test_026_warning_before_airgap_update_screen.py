import os
from unittest.mock import patch, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.warning_before_airgap_update_screen import (
    WarningBeforeAirgapUpdateScreen,
)


class TestWarningBeforeAirgapUpdateScreen(GraphicUnitTest):

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
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = WarningBeforeAirgapUpdateScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        warn = grid.children[1]
        button = grid.children[0]

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "WarningBeforeAirgapUpdateScreen")
        self.assertEqual(screen.id, "warning_before_airgap_update_screen")
        self.assertEqual(grid.id, "warning_before_airgap_update_screen_grid")
        self.assertEqual(warn.id, "warning_before_airgap_update_screen_warn")
        self.assertEqual(button.id, "warning_before_airgap_update_screen_label")

        text = "".join(
            [
                "[color=#efcc00]Before proceeding with the air-gapped update:[/color]",
                "\n",
                "* Insert a FAT32 formatted SDCard into your computer",
                "\n",
                "* On the next screen, choose the drive to copy firmware",
                "\n",
                "\n",
                "[color=#ff0000][ref=MainScreen]Back[/ref][/color]        [color=#00ff00][ref=AirgapUpdateScreen]Proceed[/ref][/color]",
            ]
        )

        self.assertEqual(button.text, text)
        mock_get_locale.assert_any_call()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_back(self, mock_set_screen, mock_get_locale):
        screen = WarningBeforeAirgapUpdateScreen()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("MainScreen")

        mock_set_screen.assert_called_once_with(name="MainScreen", direction="left")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_update(self, mock_get_locale):
        screen = WarningBeforeAirgapUpdateScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="locale", value="en_US.UTF-8")

        mock_get_locale.assert_any_call()

    @patch("sys.platform", "linux")
    # @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.on_get_removable_drives_linux",
        return_value=[],
    )
    def test_on_ref_press_no_drives_found_linux(
        self, mock_on_get_removable_drives_linux, mock_get_locale
    ):
        screen = WarningBeforeAirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        # self.render(screen)

        # get your Window instance safely
        # EventLoop.ensure_window()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("AirgapUpdateScreen")

        mock_get_locale.assert_any_call()
        mock_on_get_removable_drives_linux.assert_called_once()

    @patch("sys.platform", "darwin")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.on_get_removable_drives_macos",
        return_value=[],
    )
    def test_on_ref_press_no_drives_found_darwin(
        self, on_get_removable_drives_macos, mock_get_locale
    ):
        screen = WarningBeforeAirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("AirgapUpdateScreen")

        mock_get_locale.assert_any_call()
        on_get_removable_drives_macos.assert_called_once()

    @patch("sys.platform", "win32")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.on_get_removable_drives_windows",
        return_value=[],
    )
    def test_on_ref_press_no_drives_found_windows(
        self, on_get_removable_drives_windows, mock_get_locale
    ):
        screen = WarningBeforeAirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("AirgapUpdateScreen")

        mock_get_locale.assert_any_call()
        on_get_removable_drives_windows.assert_called_once()

    @patch("sys.platform", "linux")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.on_get_removable_drives_linux",
        return_value=["/media/mock"],
    )
    @patch("src.app.screens.warning_before_airgap_update_screen.partial")
    @patch("src.app.screens.warning_before_airgap_update_screen.Clock.schedule_once")
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_drives_found_linux(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_on_get_removable_drives_linux,
        mock_get_locale,
    ):
        screen = WarningBeforeAirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("AirgapUpdateScreen")

        mock_get_locale.assert_any_call()
        mock_on_get_removable_drives_linux.assert_called_once()
        screen.manager.get_screen.assert_called_once_with("AirgapUpdateScreen")
        mock_partial.assert_called()
        mock_schedule_once.assert_called()
        mock_set_screen.assert_called_once_with(
            name="AirgapUpdateScreen", direction="right"
        )

    @patch("sys.platform", "darwin")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.on_get_removable_drives_macos",
        return_value=["/Volumes/mock"],
    )
    @patch("src.app.screens.warning_before_airgap_update_screen.partial")
    @patch("src.app.screens.warning_before_airgap_update_screen.Clock.schedule_once")
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_drives_found_macos(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_on_get_removable_drives_macos,
        mock_get_locale,
    ):
        screen = WarningBeforeAirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("AirgapUpdateScreen")

        mock_get_locale.assert_any_call()
        mock_on_get_removable_drives_macos.assert_called_once()
        screen.manager.get_screen.assert_called_once_with("AirgapUpdateScreen")
        mock_partial.assert_called()
        mock_schedule_once.assert_called()
        mock_set_screen.assert_called_once_with(
            name="AirgapUpdateScreen", direction="right"
        )

    @patch("sys.platform", "win32")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.on_get_removable_drives_windows",
        return_value=["D:\\"],
    )
    @patch("src.app.screens.warning_before_airgap_update_screen.partial")
    @patch("src.app.screens.warning_before_airgap_update_screen.Clock.schedule_once")
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_drives_found_windows(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_on_get_removable_drives_windows,
        mock_get_locale,
    ):
        screen = WarningBeforeAirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        action = getattr(
            screen, "on_ref_press_warning_before_airgap_update_screen_label"
        )
        action("AirgapUpdateScreen")

        mock_get_locale.assert_any_call()
        mock_on_get_removable_drives_windows.assert_called_once()
        screen.manager.get_screen.assert_called_once_with("AirgapUpdateScreen")
        mock_partial.assert_called()
        mock_schedule_once.assert_called()
        mock_set_screen.assert_called_once_with(
            name="AirgapUpdateScreen", direction="right"
        )

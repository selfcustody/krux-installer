import os
from unittest.mock import MagicMock, call, patch

from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.core.text import DEFAULT_FONT, LabelBase
from kivy.tests.common import GraphicUnitTest

from src.app.screens.main_screen import MainScreen


class TestMainScreen(GraphicUnitTest):
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
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "MainScreen")
        self.assertEqual(screen.id, "main_screen")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_grid_layout(self, mock_get_locale):
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.get = MagicMock(return_value="en-US")
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "main_screen_grid")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_buttons(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        # New layout: 5 buttons — select_device, flash, wipe, settings, about
        self.assertEqual(len(buttons), 5)
        self.assertEqual(buttons[4].id, "main_select_device")
        self.assertEqual(buttons[3].id, "main_flash")
        self.assertEqual(buttons[2].id, "main_wipe")
        self.assertEqual(buttons[1].id, "main_settings")
        self.assertEqual(buttons[0].id, "main_about")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_press_cant_flash_or_wipe(self, mock_get_locale, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []
        for button in grid.children:
            action = getattr(screen.__class__, f"on_press_{button.id}")
            action(button)
            if button.id in ("main_select_device", "main_settings", "main_about"):
                calls.append(call(wid=button.id, rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.open_settings")
    def test_on_release_cant_flash_or_wipe(
        self,
        mock_open_settings,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_set_screen = []

        for button in grid.children:
            action = getattr(screen.__class__, f"on_release_{button.id}")
            action(button)

            if button.id in ("main_select_device", "main_settings", "main_about"):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 1)))

            if button.id == "main_select_device":
                calls_set_screen.append(
                    call(name="SelectDeviceScreen", direction="left")
                )

            if button.id == "main_about":
                calls_set_screen.append(call(name="AboutScreen", direction="left"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_get_locale.assert_any_call()
        mock_open_settings.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_device(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]select a new one[/color]"
        )
        initial_flash_text = flash_button.text
        initial_wipe_text = wipe_button.text
        self.assertIn("color=#333333", initial_flash_text)
        self.assertIn("color=#333333", initial_wipe_text)

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectDeviceScreen", key="device", value=device)
            mocked_text_device = f"Device: [color=#00AABB]{device}[/color]"
            self.assertEqual(device_button.text, mocked_text_device)
            self.assertNotIn("color=#333333", flash_button.text)
            self.assertNotIn("color=#333333", wipe_button.text)

        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_device(self, mock_redirect_exception, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()

        screen.update(name="SelectDeviceScreen", key="device")
        mock_redirect_exception.assert_called()
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_invalid_screen(self, mock_redirect_exception, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        screen.update(name="MockedScreen", key="device", value="m5stickv")

        mock_get_locale.assert_any_call()
        mock_redirect_exception.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_fail_update_invalid_key(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()

        screen.update(name="SelectDeviceScreen", key="mock", value="mock")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_no_valid_device_but_valid_situation(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        text_device = "Device: [color=#00AABB]select a new one[/color]"
        self.assertEqual(device_button.text, text_device)
        self.assertIn("color=#333333", flash_button.text)
        self.assertIn("color=#333333", wipe_button.text)

        screen.update(name="SelectDeviceScreen", key="device", value="Mocked device")

        mocked_text_device = "Device: [color=#00AABB]Mocked device[/color]"
        self.assertEqual(device_button.text, mocked_text_device)
        self.assertIn("color=#333333", flash_button.text)
        self.assertIn("color=#333333", wipe_button.text)

        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()

        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        self.assertEqual(screen.locale, "en_US.UTF-8")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_device_select_a_new_one(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]

        screen.update(
            name="ConfigKruxInstaller", key="device", value="select a new one"
        )
        text_device = "Device: [color=#00AABB]select a new one[/color]"
        self.assertEqual(screen.device, "select a new one")
        self.assertEqual(device_button.text, text_device)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_not_will_flash(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="ConfigKruxInstaller", key="flash", value=None)

        self.assertTrue(flash_button.markup)
        self.assertIn("color=#333333", flash_button.text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_will_flash(self, mock_get_locale):
        screen = MainScreen()
        screen.will_flash = True
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="ConfigKruxInstaller", key="flash", value=None)

        self.assertNotIn("color=#333333", flash_button.text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_not_will_wipe(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        wipe_button = grid.children[2]

        screen.update(name="ConfigKruxInstaller", key="wipe", value=None)

        self.assertIn("color=#333333", wipe_button.text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_will_wipe(self, mock_get_locale):
        screen = MainScreen()
        screen.will_wipe = True
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        wipe_button = grid.children[2]

        screen.update(name="ConfigKruxInstaller", key="wipe", value=None)

        self.assertNotIn("color=#333333", wipe_button.text)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_settings(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        s_button = grid.children[1]

        screen.update(name="ConfigKruxInstaller", key="settings", value=None)

        self.assertEqual(s_button.text, "Settings")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_about(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        a_button = grid.children[0]

        screen.update(name="ConfigKruxInstaller", key="about", value=None)
        self.assertEqual(a_button.text, "About")
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_press_can_flash_or_wipe(self, mock_get_locale, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        background_calls = []

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectDeviceScreen", key="device", value=device)
            flash_action = getattr(screen.__class__, f"on_press_{flash_button.id}")
            wipe_action = getattr(screen.__class__, f"on_press_{wipe_button.id}")
            flash_action(flash_button)
            wipe_action(wipe_button)
            background_calls.append(call(wid="main_flash", rgba=(0.25, 0.25, 0.25, 1)))
            background_calls.append(call(wid="main_wipe", rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(background_calls)
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_release_flash_goes_to_flash_screen(
        self,
        mock_get_running_app,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_app = MagicMock()
        mock_app.config.get.return_value = "1500000"
        mock_get_running_app.return_value = mock_app
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        screen.update(name="SelectDeviceScreen", key="device", value="m5stickv")
        action = getattr(screen.__class__, f"on_release_{button.id}")
        action(button)

        mock_get_locale.assert_any_call()
        mock_set_background.assert_called_once_with(wid="main_flash", rgba=(0, 0, 0, 1))
        mock_set_screen.assert_called_once_with(name="FlashScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_on_release_flash_invalid_device(
        self,
        mock_redirect_exception,
        mock_get_locale,
        mock_manager,
        _mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[3]

        screen.will_flash = True
        screen.device = "invalid_device"
        action = getattr(screen.__class__, f"on_release_{button.id}")
        action(button)

        mock_get_locale.assert_any_call()
        mock_redirect_exception.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_release_wipe(
        self,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        button = grid.children[2]

        calls_set_background = []
        calls_set_screen = []

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectDeviceScreen", key="device", value=device)
            action = getattr(screen.__class__, f"on_release_{button.id}")
            action(button)

            calls_set_background.append(call(wid="main_wipe", rgba=(0, 0, 0, 1)))
            calls_set_screen.append(call(name="WarningWipeScreen", direction="left"))

        mock_get_locale.assert_any_call()
        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)

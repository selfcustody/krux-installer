import re
from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.main_screen import MainScreen


class TestMainScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_main_screen(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "MainScreen")
        self.assertEqual(screen.id, "main_screen")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_grid_layout(self, mock_get_locale):
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.get = MagicMock(return_value="en-US")
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        self.assertEqual(grid.id, "main_screen_grid")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_render_buttons(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        buttons = grid.children

        self.assertEqual(len(buttons), 6)
        self.assertEqual(buttons[5].id, "main_select_version")
        self.assertEqual(buttons[4].id, "main_select_device")
        self.assertEqual(buttons[3].id, "main_flash")
        self.assertEqual(buttons[2].id, "main_wipe")
        self.assertEqual(buttons[1].id, "main_settings")
        self.assertEqual(buttons[0].id, "main_about")

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_press_cant_flash_or_wipe(self, mock_get_locale, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls = []
        for button in grid.children:
            action = getattr(screen, f"on_press_{button.id}")
            action(button)
            if button.id in (
                "main_select_device",
                "main_select_version",
                "main_settings",
                "main_about",
            ):
                calls.append(call(wid=button.id, rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_called_once()

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

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        calls_set_background = []
        calls_set_screen = []
        calls_manager = []

        for button in grid.children:
            action = getattr(screen, f"on_release_{button.id}")
            action(button)

            if button.id in (
                "main_select_device",
                "main_select_version",
                "main_settings",
                "main_about",
            ):
                calls_set_background.append(call(wid=button.id, rgba=(0, 0, 0, 1)))

            if button.id == "main_select_device":
                calls_set_screen.append(
                    call(name="SelectDeviceScreen", direction="left")
                )
                calls_manager.append(call("SelectDeviceScreen"))

            if button.id == "main_select_version":
                calls_set_screen.append(
                    call(name="SelectVersionScreen", direction="left")
                )
                calls_manager.append(call("SelectVersionScreen"))
                calls_manager.append(call().clear())
                calls_manager.append(call().fetch_releases())
            if button.id == "main_about":
                calls_set_screen.append(call(name="AboutScreen", direction="left"))

        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)
        mock_manager.get_screen.assert_has_calls(calls_manager)
        mock_get_locale.assert_called_once()
        mock_open_settings.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_version(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[5]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(
            device_button.text, "Version: [color=#00AABB]select a new one[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Update firmware[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe device[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)

        for version in (
            "odudex/krux_binaries",
            "v23.09.1",
            "v23.09.0",
            "v22.08.2",
            "v22.08.1",
            "v22.08.0",
            "v22.03.0",
        ):
            screen.update(name="SelectVersionScreen", key="version", value=version)
            self.assertEqual(
                device_button.text, f"Version: [color=#00AABB]{version}[/color]"
            )
            self.assertEqual(
                flash_button.text, "[color=#333333]Update firmware[/color]"
            )
            self.assertEqual(wipe_button.text, "[color=#333333]Wipe device[/color]")
            self.assertTrue(flash_button.markup)
            self.assertTrue(wipe_button.markup)

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_device(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]select a new one[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Update firmware[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe device[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectVersionScreen", key="device", value=device)
            self.assertEqual(
                device_button.text, f"Device: [color=#00AABB]{device}[/color]"
            )
            self.assertEqual(flash_button.text, "Update firmware")
            self.assertEqual(wipe_button.text, "Wipe device")
            self.assertFalse(flash_button.markup)
            self.assertFalse(wipe_button.markup)

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_fail_update_invalid_screen(self, mock_redirect_error, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name="MockedScreen", key="device", value="v24.03.0")

        mock_get_locale.assert_called_once()
        mock_redirect_error.assert_called_once_with(
            msg="Invalid screen name: MockedScreen"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_error")
    def test_fail_update_invalid_key(self, mock_redirect_error, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="SelectDeviceScreen", key="mock", value="mock")
        mock_get_locale.assert_called_once()
        mock_redirect_error.assert_called_once_with(msg='Invalid key: "mock"')

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_no_valid_device_but_valid_situation(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]select a new one[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Update firmware[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe device[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)

        screen.update(name="SelectDeviceScreen", key="device", value="Mocked device")

        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]Mocked device[/color]"
        )
        self.assertEqual(flash_button.text, "[color=#333333]Update firmware[/color]")
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe device[/color]")
        self.assertTrue(flash_button.markup)
        self.assertTrue(wipe_button.markup)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        self.assertEqual(screen.locale, "en_US.UTF-8")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_device_select_a_new_one(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        device_button = grid.children[4]

        screen.update(
            name="ConfigKruxInstaller", key="device", value="select a new one"
        )
        self.assertEqual(screen.device, "select a new one")
        self.assertEqual(
            device_button.text, "Device: [color=#00AABB]select a new one[/color]"
        )
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_not_will_flash(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="ConfigKruxInstaller", key="flash", value=None)

        self.assertTrue(flash_button.markup)
        self.assertEqual(flash_button.text, "[color=#333333]Update firmware[/color]")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_will_flash(self, mock_get_locale):
        screen = MainScreen()
        screen.will_flash = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="ConfigKruxInstaller", key="flash", value=None)

        self.assertFalse(flash_button.markup)
        self.assertEqual(flash_button.text, "Update firmware")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_not_will_wipe(self, mock_get_locale):
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.get = MagicMock(return_value="en-US")

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        wipe_button = grid.children[2]

        screen.update(name="ConfigKruxInstaller", key="wipe", value=None)

        self.assertTrue(wipe_button.markup)
        self.assertEqual(wipe_button.text, "[color=#333333]Wipe device[/color]")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_flash_will_wipe(self, mock_get_locale):
        screen = MainScreen()
        screen.will_wipe = True
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        wipe_button = grid.children[2]

        screen.update(name="ConfigKruxInstaller", key="wipe", value=None)

        self.assertFalse(wipe_button.markup)
        self.assertEqual(wipe_button.text, "Wipe device")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_settings(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        s_button = grid.children[1]

        screen.update(name="ConfigKruxInstaller", key="settings", value=None)

        self.assertEqual(s_button.text, "Settings")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_about(self, mock_get_locale):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        a_button = grid.children[0]

        screen.update(name="ConfigKruxInstaller", key="about", value=None)

        self.assertEqual(a_button.text, "About")
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_press_can_flash_or_wipe(self, mock_get_locale, mock_set_background):
        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]
        wipe_button = grid.children[2]

        calls = []

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectVersionScreen", key="device", value=device)
            flash_action = getattr(screen, "on_press_main_flash")
            wipe_action = getattr(screen, "on_press_main_wipe")
            flash_action(flash_button)
            wipe_action(wipe_button)
            calls.append(call(wid="main_flash", rgba=(0.25, 0.25, 0.25, 1)))
            calls.append(call(wid="main_wipe", rgba=(0.25, 0.25, 0.25, 1)))

        mock_set_background.assert_has_calls(calls)
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.get_destdir_assets")
    @patch("src.app.screens.main_screen.re.findall", side_effect=[True])
    @patch("src.app.screens.main_screen.os.path.isfile", side_effect=[False])
    def test_on_release_flash_to_download_stable_zip_screen(
        self,
        mock_isfile,
        mock_findall,
        mock_get_destdir_assets,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        screen.version = "v24.03.0"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="SelectVersionScreen", key="device", value="m5stickv")
        flash_action = getattr(screen, "on_release_main_flash")
        flash_action(flash_button)

        mock_get_locale.assert_called_once()
        mock_get_destdir_assets.assert_called_once()
        mock_set_background.assert_called_once_with(wid="main_flash", rgba=(0, 0, 0, 1))
        mock_set_screen.assert_called_once_with(
            name="DownloadStableZipScreen", direction="left"
        )
        mock_findall.assert_called_once_with(r"^v\d+\.\d+\.\d$", "v24.03.0")
        pattern = re.compile(r".*v24\.03\.0\.zip")
        self.assertTrue(pattern.match(mock_isfile.call_args[0][0]))

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.get_destdir_assets")
    @patch("src.app.screens.main_screen.re.findall", side_effect=[True])
    @patch("src.app.screens.main_screen.os.path.isfile", side_effect=[True])
    def test_on_release_flash_to_warning_already_downloaded_zip_screen(
        self,
        mock_isfile,
        mock_findall,
        mock_get_destdir_assets,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        screen.version = "v24.03.0"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="SelectVersionScreen", key="device", value="m5stickv")
        flash_action = getattr(screen, "on_release_main_flash")
        flash_action(flash_button)

        mock_get_locale.assert_called_once()
        mock_get_destdir_assets.assert_called_once()
        mock_set_background.assert_called_once_with(wid="main_flash", rgba=(0, 0, 0, 1))
        mock_set_screen.assert_called_once_with(
            name="WarningAlreadyDownloadedScreen", direction="left"
        )
        mock_findall.assert_called_once_with(r"^v\d+\.\d+\.\d$", "v24.03.0")
        pattern = re.compile(r".*v24\.03\.0\.zip")
        self.assertTrue(pattern.match(mock_isfile.call_args[0][0]))

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.main_screen.re.findall", side_effect=[False, True])
    def test_on_release_flash_to_download_beta_screen(
        self,
        mock_findall,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        screen.version = "odudex/krux_binaries"
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        flash_button = grid.children[3]

        screen.update(name="SelectVersionScreen", key="device", value="m5stickv")
        flash_action = getattr(screen, "on_release_main_flash")
        flash_action(flash_button)

        mock_get_locale.assert_called_once()
        mock_findall.assert_has_calls(
            [
                call("^v\\d+\\.\\d+\\.\\d$", "odudex/krux_binaries"),
                call(r"^odudex/krux_binaries", "odudex/krux_binaries"),
            ]
        )
        mock_set_background.assert_called_once_with(wid="main_flash", rgba=(0, 0, 0, 1))
        mock_set_screen.assert_called_once_with(
            name="DownloadBetaScreen", direction="left"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.MainScreen.set_background")
    @patch("src.app.screens.main_screen.MainScreen.set_screen")
    @patch("src.app.screens.main_screen.MainScreen.manager")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.get_baudrate", return_value=1500000)
    def test_on_release_wipe(
        self,
        mock_get_baudrate,
        mock_get_locale,
        mock_manager,
        mock_set_screen,
        mock_set_background,
    ):
        mock_manager.get_screen = MagicMock()

        screen = MainScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        wipe_button = grid.children[2]

        calls_set_background = []
        calls_set_screen = []

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            screen.update(name="SelectVersionScreen", key="device", value=device)
            wipe_action = getattr(screen, "on_release_main_wipe")
            wipe_action(wipe_button)

            calls_set_background.append(call(wid="main_wipe", rgba=(0, 0, 0, 1)))
            calls_set_screen.append(call(name="WipeScreen", direction="left"))

        mock_get_baudrate.assert_called()
        mock_get_locale.assert_called_once()
        mock_set_background.assert_has_calls(calls_set_background)
        mock_set_screen.assert_has_calls(calls_set_screen)

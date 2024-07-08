from unittest.mock import patch, call, MagicMock
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.warning_already_downloaded_screen import (
    WarningAlreadyDownloadedScreen,
)


class TestWarningAlreadyDownloadedScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_init(self, mock_get_running_app):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        label = grid.children[1]
        stack = grid.children[0]

        # default assertions
        self.assertEqual(grid.id, f"{screen.id}_grid")
        self.assertEqual(label.id, f"{screen.id}_label")
        self.assertEqual(stack.id, f"{screen.id}_stack_buttons")
        self.assertEqual(stack.children[1].id, f"{screen.id}_download_button")
        self.assertEqual(stack.children[0].id, f"{screen.id}_proceed_button")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_invalid_name(self, mock_get_running_app):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="MockScreen")

        # default assertions
        self.assertEqual(str(exc_info.exception), "Invalid screen name: MockScreen")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_key(self, mock_get_running_app):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        with self.assertRaises(ValueError) as exc_info:
            screen.update(name=screen.name, key="mock")

        # default assertions
        self.assertEqual(str(exc_info.exception), 'Invalid key: "mock"')

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_locale(self, mock_get_running_app):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_version(self, mock_get_running_app):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.configure_mock(**attrs)

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        label_text = "\n".join(
            [
                "",
                "",
                "",
                "",
                "",
                "",
                "[size=36sp][color=#efcc00][b]Assets already downloaded[/b][/color][/size]",
                "",
                "",
                "",
                "[size=20sp][color=#efcc00]krux-v0.0.1.zip[/color][/size]",
                "",
                "[size=20sp][color=#efcc00]krux-v0.0.1.zip.sha256.txt[/color][/size]",
                "",
                "[size=20sp][color=#efcc00]krux-v0.0.1.zip.sig[/color][/size]",
                "",
                "[size=20sp][color=#efcc00]selfcustody.pem[/color][/size]",
                "",
                "",
                "",
                "[size=16sp]Do you want to proceed with the same file or do you want to download it again?[/size]",
                "",
                "",
                "",
            ]
        )
        download_text = "[color=#00ff00]Download again[/color]"
        proceed_text = "[color=#00ccef]Proceed with files[/color]"

        screen.update(name=screen.name, key="version", value="v0.0.1")

        # default assertions
        self.assertEqual(screen.ids[f"{screen.id}_download_button"].text, download_text)
        self.assertEqual(screen.ids[f"{screen.id}_proceed_button"].text, proceed_text)
        self.assertEqual(screen.ids[f"{screen.id}_label"].text, label_text)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_background"
    )
    def test_on_press_donwload_button(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_download_button"]

        action = getattr(screen, f"on_press_{screen.id}_download_button")
        action(button)

        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.25, 0.25, 0.25, 1)
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_background"
    )
    def test_on_press_proceed_button(self, mock_set_background, mock_get_running_app):
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_proceed_button"]

        action = getattr(screen, f"on_press_{screen.id}_proceed_button")
        action(button)

        mock_set_background.assert_called_once_with(
            wid=button.id, rgba=(0.25, 0.25, 0.25, 1)
        )
        mock_get_running_app.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_background"
    )
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.manager"
    )
    @patch("src.app.screens.warning_already_downloaded_screen.partial")
    @patch("src.app.screens.warning_already_downloaded_screen.Clock.schedule_once")
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_screen"
    )
    def test_on_release_download(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_manager,
        mock_set_background,
        mock_get_running_app,
    ):

        mock_manager.get_screen = MagicMock()
        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_download_button"]

        action = getattr(screen, f"on_release_{screen.id}_download_button")
        action(button)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )

        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 1))
        mock_manager.get_screen.assert_has_calls(
            [call("MainScreen"), call("DownloadStableZipScreen")]
        )
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(
                    mock_manager.get_screen().update,
                    name=screen.name,
                    key="version",
                    value=mock_manager.get_screen().version,
                ),
            ]
        )
        mock_schedule_once.assert_has_calls(
            [call(mock_partial(), 0), call(mock_partial(), 0)]
        )
        mock_set_screen.assert_called_once_with(
            name="DownloadStableZipScreen", direction="right"
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.main_screen.App.get_running_app")
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_background"
    )
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_screen"
    )
    def test_on_release_proceed(
        self, mock_set_screen, mock_set_background, mock_get_running_app
    ):

        mock_get_running_app.config = MagicMock()
        mock_get_running_app.config.get = MagicMock(return_value="en-US")

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_proceed_button"]

        action = getattr(screen, f"on_release_{screen.id}_proceed_button")
        action(button)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")],
            any_order=True,
        )
        mock_set_background.assert_called_once_with(wid=button.id, rgba=(0, 0, 0, 1))
        mock_set_screen.assert_called_once_with(
            name="VerifyStableZipScreen", direction="right"
        )

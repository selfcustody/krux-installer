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
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # default assertions
        self.assertTrue(f"{screen.id}_grid" in screen.ids)
        self.assertTrue(f"{screen.id}_label" in screen.ids)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_invalid_name(self, mock_redirect_exception, mock_get_locale):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="MockScreen")

        # patch assertions
        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # do tests
        screen.update(name="ConfigKruxInstaller", key="locale", value="en_US.UTF-8")

        # default assertions
        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_version(self, mock_get_locale):
        attrs = {"get.side_effect": ["en-US.UTF8", "mockdir"]}
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.configure_mock(**attrs)

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        label_text = "".join(
            [
                "[color=#efcc00][b]Assets already downloaded[/b][/color]",
                "\n",
                "* krux-v0.0.1.zip",
                "\n",
                "* krux-v0.0.1.zip.sha256.txt",
                "\n",
                "* krux-v0.0.1.zip.sig",
                "\n",
                "* selfcustody.pem",
                "\n",
                "\n",
                "[color=#00ff00]",
                "[ref=DownloadStableZipScreen]",
                "[u]Download again[/u]",
                "[/ref]",
                "[/color]",
                "        ",
                "[color=#efcc00]",
                "[ref=VerifyStableZipScreen]",
                "[u]Proceed with current file[/u]",
                "[/ref]",
                "[/color]",
            ]
        )

        screen.update(name=screen.name, key="version", value="v0.0.1")

        # default assertions
        self.assertEqual(screen.ids[f"{screen.id}_label"].text, label_text)

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.manager"
    )
    @patch("src.app.screens.warning_already_downloaded_screen.partial")
    @patch("src.app.screens.warning_already_downloaded_screen.Clock.schedule_once")
    def test_on_press_donwload_button(
        self, mock_schedule_once, mock_partial, mock_manager, mock_get_locale
    ):
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.get = MagicMock(return_value="en-US")

        mock_manager.get_screen = MagicMock()

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(button, "DownloadStableZipScreen")

        mock_get_locale.assert_any_call()
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
        mock_schedule_once.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.warning_already_downloaded_screen.WarningAlreadyDownloadedScreen.set_screen"
    )
    def test_on_press_proceed(self, mock_set_screen, mock_get_locale):
        mock_get_locale.config = MagicMock()
        mock_get_locale.config.get = MagicMock(return_value="en-US")

        screen = WarningAlreadyDownloadedScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        button = screen.ids[f"{screen.id}_label"]

        action = getattr(screen.__class__, f"on_ref_press_{button.id}")
        action(button, "VerifyStableZipScreen")

        mock_get_locale.assert_any_call()
        mock_set_screen.assert_called_once_with(
            name="VerifyStableZipScreen", direction="left"
        )

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from pytest import mark
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.greetings_screen import GreetingsScreen


class TestAboutScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]
        image = grid.children[0]

        # default assertions
        root = Path(__file__).parent.parent
        asset = os.path.join(root, "assets", "logo.png")
        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "GreetingsScreen")
        self.assertEqual(screen.id, "greetings_screen")
        self.assertEqual(image.source, asset)
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_on_enter(self, mock_schedule_once, mock_partial, mock_get_locale):
        screen = GreetingsScreen()
        self.render(screen)
        screen.on_enter()

        # get your Window instance safely
        EventLoop.ensure_window()

        mock_get_locale.assert_called()
        mock_partial.assert_called()
        mock_schedule_once.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.GreetingsScreen.check_permissions_for_dialout_group"
    )
    def test_update_check_permission_screen(
        self, mock_check_permissions, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-permission")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_check_permissions.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.check_internet_connection")
    def test_update_check_internet_connection(
        self, mock_check_internet, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-internet-connection")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_check_internet.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.manager")
    @patch("src.app.screens.greetings_screen.Selector")
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.set_screen")
    def test_check_internet_connection(
        self,
        mock_set_screen,
        mock_schedule_once,
        mock_partial,
        mock_selector,
        mock_manager,
        mock_get_locale,
    ):
        mock_manager.get_screen = MagicMock()
        mock_manager.get_screen.update = MagicMock()
        mock_selector.return_value = MagicMock(releases=["v0.0.1"])
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-internet-connection")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_manager.get_screen.assert_called_once()
        mock_partial.assert_called_once_with(
            mock_manager.get_screen().update,
            name="GreetingsScreen",
            key="version",
            value="v0.0.1",
        )
        mock_schedule_once.assert_called()
        mock_set_screen.assert_called_once_with(name="MainScreen", direction="left")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.greetings_screen.Selector", side_effect=[Exception("Mocked")]
    )
    @patch("src.app.screens.greetings_screen.GreetingsScreen.redirect_exception")
    def test_fail_check_internet_connection(
        self, mock_redirect_exception, mock_selector, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-internet-connection")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_selector.assert_called()
        mock_redirect_exception.assert_called()

    @patch("sys.platform", "win32")
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.partial")
    @patch("src.app.screens.greetings_screen.Clock.schedule_once")
    def test_pass_check_permissions_not_linux(
        self, mock_schedule_once, mock_partial, mock_get_locale
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-permission")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_partial.assert_called_once_with(
            screen.update, name="GreetingsScreen", key="check-internet-connection"
        )
        mock_schedule_once.assert_called()

    @mark.skipif(
        sys.platform in ("win32", "darwin"),
        reason="does not run on windows or darwin",
    )
    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.greetings_screen.os.environ.get", return_value="mockuser")
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.greetings_screen.distro.id", return_value="mockos")
    @patch("src.app.screens.greetings_screen.GreetingsScreen.redirect_exception")
    def test_fail_check_permission_linux(
        self, mock_redirect_exception, mock_distro_id, mock_get_locale, mock_environ_get
    ):
        screen = GreetingsScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name=screen.name, key="check-permission")

        # patch assertions
        mock_environ_get.assert_called_once()
        mock_get_locale.assert_called_once()
        mock_distro_id.assert_called_once()
        mock_redirect_exception.assert_called_once()

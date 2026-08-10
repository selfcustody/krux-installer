import os
from pathlib import Path
from unittest.mock import MagicMock, patch

from kivy.base import EventLoop, EventLoopBase
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest

from src.app.screens.disclaimer_screen import DisclaimerScreen


class TestDisclaimerScreen(GraphicUnitTest):
    @classmethod
    def teardown_class(cls):
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_init(self, mock_get_locale):
        screen = DisclaimerScreen()
        self.render(screen)

        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        root = Path(__file__).parent.parent
        asset = os.path.join(root, "assets", "warning.png")

        self.assertEqual(window.children[0], screen)
        self.assertEqual(screen.name, "DisclaimerScreen")
        self.assertEqual(screen.id, "disclaimer_screen")
        self.assertEqual(len(grid.children), 2)
        self.assertEqual(screen.ids["disclaimer_screen_warn"].source, asset)
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_renders_disclaimer(self, mock_get_locale):
        screen = DisclaimerScreen()
        self.render(screen)

        EventLoop.ensure_window()

        text = screen.ids["disclaimer_screen_label"].text

        self.assertIn(
            "Krux is a research and development project, made by nerds "
            "building tools for their own interests, open to the world.",
            text,
        )
        self.assertIn(
            "Innovative features may have undiscovered flaws that endanger funds.",
            text,
        )
        self.assertIn("[color=#EFCC00]Use it at your own risk.[/color]", text)

        # neither choice is nudged, so both refs share the plain text color
        self.assertIn("[color=#ffffff][ref=Close][u]Close[/u][/ref][/color]", text)
        self.assertIn(
            "[color=#ffffff][ref=IUnderstand][u]I understand[/u][/ref][/color]",
            text,
        )
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.disclaimer_screen.DisclaimerScreen.quit_app")
    def test_on_ref_press_close_quits_app(self, mock_quit_app, mock_get_locale):
        screen = DisclaimerScreen()
        self.render(screen)

        EventLoop.ensure_window()

        action = getattr(DisclaimerScreen, "on_ref_press_disclaimer_screen_label")
        action(screen.ids["disclaimer_screen_label"], "Close")

        mock_quit_app.assert_called_once()
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.manager")
    @patch("src.app.screens.disclaimer_screen.Clock.schedule_once")
    def test_on_ref_press_i_understand_checks_permission(
        self, mock_schedule_once, mock_manager, mock_get_locale
    ):
        greetings = MagicMock()
        mock_manager.get_screen = MagicMock(return_value=greetings)

        screen = DisclaimerScreen()
        self.render(screen)

        EventLoop.ensure_window()

        action = getattr(DisclaimerScreen, "on_ref_press_disclaimer_screen_label")
        action(screen.ids["disclaimer_screen_label"], "IUnderstand")

        mock_manager.get_screen.assert_called_once_with("GreetingsScreen")

        # the dialout check is asked back from GreetingsScreen, which owns it
        scheduled = mock_schedule_once.call_args_list[-1][0][0]
        self.assertEqual(scheduled.func, greetings.update)
        self.assertEqual(
            scheduled.keywords,
            {"name": "DisclaimerScreen", "key": "check-permission"},
        )
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = DisclaimerScreen()
        self.render(screen)

        EventLoop.ensure_window()

        screen.update(name="ConfigKruxInstaller", key="locale", value="pt_BR.UTF-8")

        self.assertEqual(screen.locale, "pt_BR.UTF-8")
        self.assertIn(
            "Use por sua própria conta e risco.",
            screen.ids["disclaimer_screen_label"].text,
        )
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.disclaimer_screen.DisclaimerScreen.redirect_exception")
    def test_fail_update_invalid_screen(self, mock_redirect_exception, mock_get_locale):
        screen = DisclaimerScreen()
        self.render(screen)

        EventLoop.ensure_window()

        screen.update(name="MockScreen", key="locale", value="en_US.UTF-8")

        mock_redirect_exception.assert_called_once()
        mock_get_locale.assert_called()

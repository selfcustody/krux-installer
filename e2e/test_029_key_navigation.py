import os
from unittest.mock import patch
from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.uix.screenmanager import ScreenManager, Screen
from src.app.__init__ import KruxInstallerApp

# pylint: disable=unused-argument,protected-access


class TestAppKeyNavigation(GraphicUnitTest):
    @classmethod
    def setUpClass(cls):
        cwd_path = os.path.dirname(__file__)
        rel_assets_path = os.path.join(cwd_path, "..", "assets")
        assets_path = os.path.abspath(rel_assets_path)
        font_name = "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
        noto_sans_path = os.path.join(assets_path, font_name)
        LabelBase.register(DEFAULT_FONT, noto_sans_path)
        cls._patch_bind = patch(
            "kivy.core.window.Window.bind", new=lambda *a, **k: None
        )
        cls._patch_bind.start()

    @classmethod
    def tearDownClass(cls):
        for event in Clock.get_events():
            Clock.unschedule(event)
        if getattr(cls, "_patch_bind", None):
            try:
                cls._patch_bind.stop()
            except RuntimeError:
                pass
        EventLoop.exit()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_screen_history_updates(self, mock_destdir, mock_get_locale):
        app = KruxInstallerApp()
        sm = app.build()

        self.assertTrue(hasattr(app, "_screen_history"))

        initial = sm.current
        self.assertIn(initial, app._screen_history)
        self.assertEqual(len(app._screen_history), 1)

        app._on_current_screen(None, "MainScreen")
        self.assertEqual(app._screen_history[-1], "MainScreen")
        self.assertEqual(len(app._screen_history), 2)

        app._on_current_screen(None, "MainScreen")
        self.assertEqual(len(app._screen_history), 2)
        self.assertEqual(app._screen_history.count("MainScreen"), 1)

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_navigates_back(self, mock_destdir, mock_get_locale):
        app = KruxInstallerApp()
        sm = app.build()

        app._screen_history = ["GreetingsScreen", "MainScreen"]
        sm.current = "MainScreen"

        result = app._on_key_down(None, 27, None)

        self.assertTrue(result)
        self.assertEqual(sm.current, "GreetingsScreen")
        self.assertEqual(sm.transition.direction, "right")
        self.assertEqual(len(app._screen_history), 1)

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_esc_no_history(self, mock_destdir, mock_get_locale):
        app = KruxInstallerApp()
        sm = app.build()

        app._screen_history = ["GreetingsScreen"]
        sm.current = "GreetingsScreen"

        result = app._on_key_down(None, 27, None)

        self.assertFalse(result)
        self.assertEqual(sm.current, "GreetingsScreen")
        self.assertEqual(len(app._screen_history), 1)

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_key_down_non_esc_key(self, mock_destdir, mock_get_locale):
        app = KruxInstallerApp()
        sm = app.build()

        app._screen_history = ["GreetingsScreen", "MainScreen"]
        sm.current = "MainScreen"

        result = app._on_key_down(None, 97, None)

        self.assertFalse(result)
        self.assertEqual(sm.current, "MainScreen")
        self.assertEqual(len(app._screen_history), 2)

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_build_appends_existing_current(self, mock_destdir, mock_get_locale):
        app = KruxInstallerApp()
        sm = ScreenManager()
        screen = Screen(name="ExistingScreen")
        sm.add_widget(screen)
        sm.current = "ExistingScreen"
        app.screen_manager = sm

        sm_after = app.build()

        self.assertTrue(hasattr(app, "_screen_history"))
        self.assertIn("ExistingScreen", app._screen_history)
        self.assertEqual(app._screen_history[0], "ExistingScreen")
        self.assertIs(sm_after, app.screen_manager)

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_destdir_assets", return_value="mock"
    )
    def test_on_current_screen_initializes_when_missing_or_none(
        self, mock_destdir, mock_get_locale
    ):
        app = KruxInstallerApp()
        if hasattr(app, "_screen_history"):
            delattr(app, "_screen_history")
        app._on_current_screen(None, "NewScreen")
        self.assertTrue(hasattr(app, "_screen_history"))
        self.assertEqual(app._screen_history, ["NewScreen"])

        app._screen_history = None
        app._on_current_screen(None, "AnotherScreen")
        self.assertEqual(app._screen_history[-1], "AnotherScreen")

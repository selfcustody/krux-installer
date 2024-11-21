import os
import threading
from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.wipe_screen import WipeScreen


class TestWipeScreen(GraphicUnitTest):

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
    @patch("src.app.screens.wipe_screen.partial")
    @patch("src.app.screens.wipe_screen.Clock.schedule_once")
    def test_init(self, mock_schedule_once, mock_partial, mock_get_locale):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(grid.id, "wipe_screen_grid")
        self.assertEqual(len(grid.children), 0)
        self.assertEqual(screen.baudrate, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.is_done, False)
        self.assertEqual(screen.done, None)
        self.assertEqual(screen.output, [])

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_partial.assert_called_once_with(
            screen.update, name=screen.name, key="canvas"
        )
        mock_schedule_once.assert_has_calls([call(mock_partial(), 0)], any_order=True)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_fail_update_wrong_name(self, mock_redirect_exception, mock_get_locale):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        screen.update(name="MockScreen")

        # patch assertions
        mock_get_locale.assert_called_once()
        mock_redirect_exception.assert_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = WipeScreen()

        # get your Window instance safely
        screen.update(name=screen.name, key="locale", value="en_US.UTF-8")

        self.assertEqual(screen.locale, "en_US.UTF-8")

        # patch assertions
        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_device(self, mock_get_locale):
        screen = WipeScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="device", value="amigo")

        self.assertEqual(screen.device, "amigo")

        # patch assertions
        mock_get_locale.asset_called_once()

    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_wiper(self, mock_get_locale):
        screen = WipeScreen()

        # get your Window instance safely
        screen.update(name=screen.name, key="wiper", value=1500000)
        self.assertEqual(screen.wiper.baudrate, 1500000)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_pre_enter(self, mock_get_locale):
        screen = WipeScreen()
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        self.assertTrue(hasattr(WipeScreen, "on_data"))
        self.assertTrue(hasattr(WipeScreen, "on_done"))
        self.assertIn(f"{screen.id}_subgrid", screen.ids)
        self.assertIn(f"{screen.id}_loader", screen.ids)
        self.assertIn(f"{screen.id}_progress", screen.ids)
        self.assertIn(f"{screen.id}_info", screen.ids)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_greeting_fail_on_data_mock(self, mock_get_locale):
        screen = WipeScreen()
        screen.wiper = MagicMock()
        screen.wiper.ktool.kill = MagicMock()
        screen.wiper.ktool.checkKillExit = MagicMock()

        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(WipeScreen, "on_data")
        on_data("Greeting fail: mock")

        self.assertEqual(screen.fail_msg, "Greeting fail: mock")

        # patch assertions
        mock_get_locale.assert_called()
        screen.wiper.ktool.kill.assert_called()
        screen.wiper.ktool.checkKillExit.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_data(self, mock_get_locale):
        screen = WipeScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(WipeScreen, "on_data")
        on_data("[color=#00ff00] INFO [/color] mock")

        self.assertEqual(screen.output, ["[color=#00ff00] INFO [/color] mock"])
        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_print_callback_pop_ouput(self, mock_get_locale):
        screen = WipeScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(WipeScreen, "on_data")

        for i in range(4):
            on_data(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 4)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.wipe_screen.WipeScreen.done")
    def test_on_data_erased(self, mock_done, mock_get_locale):
        screen = WipeScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(WipeScreen, "on_data")
        on_data("[color=#00ff00] INFO [/color] SPI Flash erased.")

        self.assertEqual(
            screen.output, ["[color=#00ff00] INFO [/color] SPI Flash erased."]
        )
        # patch assertions
        mock_get_locale.assert_any_call()
        mock_done.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_done(self, mock_get_locale):
        screen = WipeScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        text = "".join(
            [
                "[b]DONE![/b]",
                "\n",
                "[color=#00FF00]",
                "[ref=Back][u]Back[/u][/ref]",
                "[/color]",
                "        ",
                "[color=#EFCC00]",
                "[ref=Quit][u]Quit[/u][/ref]",
                "[/color]",
            ]
        )
        on_done = getattr(WipeScreen, "on_done")
        on_done(0)

        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)
        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.wipe_screen.partial")
    @patch("src.app.screens.wipe_screen.threading.Thread")
    @patch("src.utils.flasher.Flasher")
    def test_on_enter(self, mock_flasher, mock_thread, mock_partial, mock_get_locale):
        mock_flasher.__class__.print_callback = MagicMock()

        screen = WipeScreen()
        screen.flasher = MagicMock()
        screen.flasher.ktool = MagicMock()
        screen.flasher.flash = MagicMock()

        screen.update(name=screen.name, key="device", value="amigo")
        screen.update(name=screen.name, key="wiper", value=1500000)
        screen.on_pre_enter()
        screen.on_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(screen.wiper.wipe, device="amigo"),
            ],
            any_order=True,
        )
        mock_thread.assert_called_once_with(name=screen.name, target=mock_partial())

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.wipe_screen.partial")
    @patch("src.app.screens.wipe_screen.threading.Thread")
    @patch("src.utils.flasher.Flasher")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_on_enter_fail_stopiteration(
        self,
        mock_redirect_exception,
        mock_flasher,
        mock_thread,
        mock_partial,
        mock_get_locale,
    ):
        mock_flasher.__class__.print_callback = MagicMock()

        screen = WipeScreen()
        screen.wiper = MagicMock()
        screen.wiper.ktool = MagicMock()
        screen.wiper.flash = MagicMock()
        setattr(WipeScreen, "on_done", MagicMock())
        setattr(WipeScreen, "on_data", MagicMock())
        setattr(WipeScreen, "on_process", MagicMock())

        # Define a custom excepthook
        def mock_excepthook(args):
            exc_type, exc_value, exc_traceback, thread = args.sequence
            self.assertTrue(issubclass(exc_type, Exception))
            self.assertEqual(str(exc_value), "StopIteration mocked")
            self.assertEqual(exc_traceback, None)
            self.assertTrue(thread is mock_thread)

        # Patch threading.excepthook with the custom hook
        with patch("threading.excepthook", mock_excepthook):
            # Call the on_enter method
            screen.on_enter()

            # Simulate the exception using ExceptHookArgs
            exc_args = threading.ExceptHookArgs(
                sequence=(
                    Exception,
                    Exception("StopIteration mocked"),
                    None,
                    mock_thread,
                )
            )
            threading.excepthook(exc_args)

        # patch assertions
        mock_get_locale.assert_called()
        mock_partial.assert_called()
        mock_thread.assert_called_once_with(name=screen.name, target=mock_partial())
        mock_redirect_exception.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.wipe_screen.partial")
    @patch("src.app.screens.wipe_screen.threading.Thread")
    @patch("src.utils.flasher.Flasher")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_on_enter_fail_cancel(
        self,
        mock_redirect_exception,
        mock_flasher,
        mock_thread,
        mock_partial,
        mock_get_locale,
    ):
        mock_flasher.__class__.print_callback = MagicMock()

        screen = WipeScreen()
        screen.wiper = MagicMock()
        screen.wiper.ktool = MagicMock()
        screen.wiper.flash = MagicMock()
        setattr(WipeScreen, "on_done", MagicMock())
        setattr(WipeScreen, "on_data", MagicMock())
        setattr(WipeScreen, "on_process", MagicMock())

        # Define a custom excepthook
        def mock_excepthook(args):
            exc_type, exc_value, exc_traceback, thread = args.sequence
            self.assertTrue(issubclass(exc_type, Exception))
            self.assertEqual(str(exc_value), "Cancel mocked")
            self.assertEqual(exc_traceback, None)
            self.assertTrue(thread is mock_thread)

        # Patch threading.excepthook with the custom hook
        with patch("threading.excepthook", mock_excepthook):
            # Call the on_enter method
            screen.on_enter()

            # Simulate the exception using ExceptHookArgs
            exc_args = threading.ExceptHookArgs(
                sequence=(
                    Exception,
                    Exception("Cancel mocked"),
                    None,
                    mock_thread,
                )
            )
            threading.excepthook(exc_args)

        # patch assertions
        mock_get_locale.assert_called()
        mock_partial.assert_called()
        mock_thread.assert_called_once_with(name=screen.name, target=mock_partial())
        mock_redirect_exception.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.wipe_screen.partial")
    @patch("src.app.screens.wipe_screen.threading.Thread")
    @patch("src.utils.flasher.Flasher")
    @patch("src.app.screens.base_screen.BaseScreen.redirect_exception")
    def test_on_enter_fail_unknow(
        self,
        mock_redirect_exception,
        mock_flasher,
        mock_thread,
        mock_partial,
        mock_get_locale,
    ):
        mock_flasher.__class__.print_callback = MagicMock()

        screen = WipeScreen()
        screen.wiper = MagicMock()
        screen.wiper.ktool = MagicMock()
        screen.wiper.flash = MagicMock()
        setattr(WipeScreen, "on_done", MagicMock())
        setattr(WipeScreen, "on_data", MagicMock())
        setattr(WipeScreen, "on_process", MagicMock())

        # Define a custom excepthook
        def mock_excepthook(args):
            exc_type, exc_value, exc_traceback, thread = args.sequence
            self.assertTrue(issubclass(exc_type, Exception))
            self.assertEqual(str(exc_value), "Unknow mocked")
            self.assertEqual(exc_traceback, None)
            self.assertTrue(thread is mock_thread)

        # Patch threading.excepthook with the custom hook
        with patch("threading.excepthook", mock_excepthook):
            # Call the on_enter method
            screen.on_enter()

            # Simulate the exception using ExceptHookArgs
            exc_args = threading.ExceptHookArgs(
                sequence=(
                    Exception,
                    Exception("Unknow mocked"),
                    None,
                    mock_thread,
                )
            )
            threading.excepthook(exc_args)

        # patch assertions
        mock_get_locale.assert_called()
        mock_partial.assert_called()
        mock_thread.assert_called_once_with(name=screen.name, target=mock_partial())
        mock_redirect_exception.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    def test_on_ref_press_back_after_done(self, mock_set_screen, mock_get_locale):
        screen = WipeScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_done = getattr(WipeScreen, "on_done")
        on_ref_press = getattr(WipeScreen, "on_ref_press_wipe_screen_info")

        on_done(0)
        on_ref_press(screen.ids["wipe_screen_info"], "Back")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_set_screen.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.quit_app")
    def test_on_ref_press_quit_after_done(self, mock_quit_app, mock_get_locale):
        screen = WipeScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_done = getattr(WipeScreen, "on_done")
        on_ref_press = getattr(WipeScreen, "on_ref_press_wipe_screen_info")

        on_done(0)
        on_ref_press(screen.ids["wipe_screen_info"], "Quit")

        # patch assertions
        mock_get_locale.assert_any_call()
        mock_quit_app.assert_called()

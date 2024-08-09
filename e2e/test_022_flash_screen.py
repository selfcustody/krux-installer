from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.flash_screen import FlashScreen


class TestFlashScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.flash_screen.partial")
    @patch("src.app.screens.flash_screen.Clock.schedule_once")
    def test_init(self, mock_schedule_once, mock_partial, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window
        grid = window.children[0].children[0]

        # default assertions
        self.assertEqual(grid.id, "flash_screen_grid")
        self.assertEqual(len(grid.children), 0)
        self.assertEqual(screen.firmware, None)
        self.assertEqual(screen.baudrate, None)
        self.assertEqual(screen.thread, None)
        self.assertEqual(screen.trigger, None)
        self.assertEqual(screen.output, None)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_partial.assert_called_once_with(
            screen.update, name=screen.name, key="canvas"
        )
        mock_schedule_once.assert_has_calls([call(mock_partial(), 0)], any_order=True)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_wrong_name(self, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.update(name="MockScreen")

        self.assertEqual(str(exc_info.exception), "Invalid screen name: MockScreen")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_update_wrong_key(self, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(ValueError) as exc_info:
            screen.update(name=screen.name, key="mock")

        self.assertEqual(str(exc_info.exception), 'Invalid key: "mock"')

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_locale(self, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="locale", value="en_US.UTF8")

        self.assertEqual(screen.locale, "en_US.UTF8")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.flash_screen.Rectangle")
    @patch("src.app.screens.flash_screen.Color")
    def test_update_canvas(self, mock_color, mock_rectangle, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        window = EventLoop.window

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_color.assert_called_once_with(0, 0, 0, 1)

        # Check why the below happens: In linux, it will set window
        # dimension to 640, 800. In Mac, it will set window 1280, 1600
        args, kwargs = mock_rectangle.call_args_list[-1]
        self.assertTrue("size" in kwargs)
        self.assertEqual(len(args), 0)
        mock_rectangle.assert_called_once_with(size=window.size)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_update_baudrate(self, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="baudrate", value=1500000)

        self.assertEqual(screen.baudrate, 1500000)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.utils.flasher.base_flasher.os.path.exists", side_effect=[True])
    def test_update_firmware(self, mock_exists, mock_get_running_app):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="firmware", value="mock.kfpkg")

        self.assertEqual(screen.firmware, "mock.kfpkg")
        mock_exists.assert_called_once_with("mock.kfpkg")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.utils.flasher.base_flasher.os.path.exists", side_effect=[True, True])
    def test_update_flasher(self, mock_exists, mock_get_running_app):
        screen = FlashScreen()
        screen.firmware = "mock.kfpkg"
        screen.baudrate = 1500000
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="flasher")

        self.assertEqual(screen.flasher.firmware, "mock.kfpkg")
        self.assertEqual(screen.flasher.baudrate, 1500000)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_exists.assert_has_calls([call("mock.kfpkg"), call("mock.kfpkg")])

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_pre_enter(self, mock_get_running_app):
        screen = FlashScreen()
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        self.assertTrue(hasattr(FlashScreen, "on_print_callback"))
        self.assertTrue(hasattr(FlashScreen, "on_process_callback"))
        self.assertTrue(hasattr(FlashScreen, "on_trigger_callback"))
        self.assertIn(f"{screen.id}_subgrid", screen.ids)
        self.assertIn(f"{screen.id}_loader", screen.ids)
        self.assertIn(f"{screen.id}_progress", screen.ids)
        self.assertIn(f"{screen.id}_info", screen.ids)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_print_callback(self, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_print_callback")
        on_print_callback("[color=#00ff00] INFO [/color] mock")

        self.assertEqual(screen.output, ["[color=#00ff00] INFO [/color] mock"])
        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_print_callback_programming_bin(self, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_print_callback")

        # Let's "print" some previous infos
        for i in range(19):
            on_print_callback(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 18)

        # Now print programming BIN
        on_print_callback("Programming BIN: |=----------| 0.21% at 21 KiB/s")
        self.assertEqual(
            screen.output[-1], "Programming BIN: |=----------| 0.21% at 21 KiB/s"
        )

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_print_callback_separator(self, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_print_callback")

        # Let's "print" some previous infos
        for i in range(19):
            on_print_callback(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 18)

        # Now print programming BIN
        on_print_callback("*")
        self.assertEqual(screen.output[-2], "*")
        self.assertEqual(screen.output[-1], "")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_print_callback_message_not_recognized(self, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_print_callback")

        # Let's "print" some previous infos

        warn = "[WARN] mock test"
        on_print_callback(warn)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_print_callback_pop_ouput(self, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_print_callback")

        for i in range(19):
            on_print_callback(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 18)

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.flash_screen.FlashScreen.trigger")
    def test_on_print_callback_rebooting(self, mock_trigger, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_print_callback")
        on_print_callback("[color=#00ff00] INFO [/color] Rebooting...\n")

        self.assertEqual(
            screen.output, ["[color=#00ff00] INFO [/color] Rebooting...\n"]
        )
        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_trigger.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_on_process_callback(self, mock_get_running_app):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        text = "\n".join(
            [
                "[size=100sp]4.76 %[/size]",
                "",
                "".join(
                    [
                        "[size=28sp]Flashing [color=#efcc00][b]firmware.bin[/b][/color] at ",
                        "[color=#efcc00][b]21 KiB/s[/b][/color][/size]",
                    ]
                ),
            ]
        )
        on_process_callback = getattr(FlashScreen, "on_process_callback")
        on_process_callback(
            file_type="firmware.bin", iteration=1, total=21, suffix="21 KiB/s"
        )

        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)
        # patch assertions

        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_trigger_callback(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        text = "\n".join(
            [
                "".join(
                    [
                        "[font=terminus]",
                        f"[size={screen.SIZE_MP}sp][b]DONE![/b][/size]",
                        "[/font]",
                    ]
                ),
                "",
                "",
                "".join(
                    [
                        "[font=terminus]",
                        f"[size={screen.SIZE_MP}sp]",
                        "[color=#00FF00][ref=Back]Back[/ref][/color]",
                        "        ",
                        "[color=#00FF00][ref=Quit]Quit[/ref][/color]",
                        "[/font]",
                    ]
                ),
            ]
        )
        on_trigger_callback = getattr(FlashScreen, "on_trigger_callback")
        on_trigger_callback(0)

        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)
        # patch assertions

        mock_get_locale.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    def test_fail_on_enter(self, mock_get_running_app):
        screen = FlashScreen()
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        with self.assertRaises(RuntimeError) as exc_info:
            screen.on_enter()

        self.assertEqual(str(exc_info.exception), "Flasher isnt configured")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.screens.base_screen.App.get_running_app")
    @patch("src.app.screens.flash_screen.partial")
    @patch("src.app.screens.flash_screen.Thread")
    @patch("src.utils.flasher.Flasher")
    def test_on_enter(
        self, mock_flasher, mock_thread, mock_partial, mock_get_running_app
    ):
        mock_flasher.__class__.print_callback = MagicMock()

        screen = FlashScreen()
        screen.flasher = MagicMock()
        screen.flasher.ktool = MagicMock()
        screen.flasher.flash = MagicMock()

        screen.on_pre_enter()
        screen.on_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        # prepare assertions
        on_process_callback = getattr(FlashScreen, "on_process_callback")

        # patch assertions
        mock_get_running_app.assert_has_calls(
            [call().config.get("locale", "lang")], any_order=True
        )
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(screen.flasher.flash, callback=on_process_callback),
            ],
            any_order=True,
        )
        mock_thread.assert_called_once_with(name=screen.name, target=mock_partial())

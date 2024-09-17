from unittest.mock import patch, MagicMock, call
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.screens.flash_screen import FlashScreen


class TestFlashScreen(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.flash_screen.partial")
    @patch("src.app.screens.flash_screen.Clock.schedule_once")
    def test_init(self, mock_schedule_once, mock_partial, mock_get_locale):
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
        self.assertEqual(screen.is_done, False)
        self.assertEqual(screen.done, None)
        self.assertEqual(screen.output, [])

        # patch assertions
        mock_get_locale.assert_called()
        mock_partial.assert_called_once_with(
            screen.update, name=screen.name, key="canvas"
        )
        mock_schedule_once.assert_has_calls([call(mock_partial(), 0)], any_order=True)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_locale(self, mock_get_locale):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="locale", value="en_US.UTF8")

        self.assertEqual(screen.locale, "en_US.UTF8")

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_baudrate(self, mock_get_locale):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="baudrate", value=1500000)

        self.assertEqual(screen.baudrate, 1500000)

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.utils.flasher.base_flasher.os.path.exists", side_effect=[True])
    def test_update_firmware(self, mock_exists, mock_get_locale):
        screen = FlashScreen()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        screen.update(name=screen.name, key="firmware", value="mock.kfpkg")

        self.assertEqual(screen.firmware, "mock.kfpkg")
        mock_exists.assert_called_once_with("mock.kfpkg")

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.utils.flasher.base_flasher.os.path.exists", side_effect=[True, True])
    def test_update_flasher(self, mock_exists, mock_get_locale):
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
        mock_get_locale.assert_called()
        mock_exists.assert_has_calls([call("mock.kfpkg"), call("mock.kfpkg")])

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_pre_enter(self, mock_get_locale):
        screen = FlashScreen()
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        self.assertTrue(hasattr(FlashScreen, "on_data"))
        self.assertTrue(hasattr(FlashScreen, "on_process"))
        self.assertTrue(hasattr(FlashScreen, "on_done"))
        self.assertIn(f"{screen.id}_subgrid", screen.ids)
        self.assertIn(f"{screen.id}_loader", screen.ids)
        self.assertIn(f"{screen.id}_progress", screen.ids)
        self.assertIn(f"{screen.id}_info", screen.ids)

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_data_mock(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(FlashScreen, "on_data")
        on_data("[color=#00ff00] INFO [/color] mock")

        self.assertEqual(screen.output, ["[color=#00ff00] INFO [/color] mock"])

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_data_programming_bin(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(FlashScreen, "on_data")

        # Let's "print" some previous infos
        for i in range(4):
            on_data(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 4)

        # Now print programming BIN
        on_data("Programming BIN: |=----------| 0.21% at 21 KiB/s")
        self.assertEqual(
            screen.output[-1], "Programming BIN: |=----------| 0.21% at 21 KiB/s"
        )

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_data(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(FlashScreen, "on_data")

        # Let's "print" some previous infos
        for i in range(4):
            on_data(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 4)

        # Now print programming BIN
        on_data("*")
        self.assertEqual(screen.output[-2], "*")
        self.assertEqual(screen.output[-1], "")

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_data_message_not_recognized(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(FlashScreen, "on_data")

        # Let's "print" some previous infos
        on_data("[WARN] mock test")

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_data_pop_ouput(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_data = getattr(FlashScreen, "on_data")

        for i in range(4):
            on_data(f"[color=#00ff00] INFO [/color] mock test message {i}")

        self.assertEqual(len(screen.output), 4)

        # patch assertions
        mock_get_locale.assert_called()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.flash_screen.FlashScreen.done")
    def test_on_print_callback_rebooting(self, mock_done, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()

        on_print_callback = getattr(FlashScreen, "on_data")
        on_print_callback("[color=#00ff00] INFO [/color] Rebooting...\n")

        self.assertEqual(
            screen.output, ["[color=#00ff00] INFO [/color] Rebooting...\n"]
        )
        # patch assertions
        mock_get_locale.assert_called()
        mock_done.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_process(self, mock_get_locale):
        screen = FlashScreen()
        screen.output = []
        screen.on_pre_enter()
        self.render(screen)

        # get your Window instance safely
        EventLoop.ensure_window()
        text = "".join(
            [
                "[b]PLEASE DO NOT UNPLUG YOUR DEVICE[/b]",
                "\n",
                "4.76 %",
                "\n",
                "Flashing ",
                "[color=#efcc00][b]firmware.bin[/b][/color] at ",
                "[color=#efcc00][b]21 KiB/s[/b][/color]",
            ]
        )
        on_process = getattr(FlashScreen, "on_process")
        on_process(file_type="firmware.bin", iteration=1, total=21, suffix="21 KiB/s")

        # default assertions
        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_done(self, mock_get_locale):
        screen = FlashScreen()
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

        on_done = getattr(FlashScreen, "on_done")
        on_done(0)

        self.assertEqual(screen.ids[f"{screen.id}_progress"].text, text)

        # patch assertions
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.flash_screen.partial")
    @patch("src.app.screens.flash_screen.threading.Thread")
    @patch("src.utils.flasher.Flasher")
    def test_on_enter(self, mock_flasher, mock_thread, mock_partial, mock_get_locale):
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
        on_process = getattr(FlashScreen, "on_process")

        # patch assertions
        mock_get_locale.assert_called()
        mock_partial.assert_has_calls(
            [
                call(screen.update, name=screen.name, key="canvas"),
                call(screen.flasher.flash, callback=on_process),
            ],
            any_order=True,
        )
        mock_thread.assert_called_once_with(name=screen.name, target=mock_partial())

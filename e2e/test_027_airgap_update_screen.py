import os
from unittest.mock import patch, MagicMock, mock_open
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from kivy.core.text import LabelBase, DEFAULT_FONT
from src.app.screens.airgap_update_screen import (
    AirgapUpdateScreen,
)

# pylint: disable=line-too-long
MOCK_SIG = b"0E\x02!\x00\xed\xfb\xb2\x99\x06\x99\x97fDQ\x0f%\xdf=\xe7^h\xd1\xb6n\x16\x9cBm\xc4\xcc\xbbb:P\xb5#\x02 f\xee\xf8\x95\xfd'sqH\x9eO\xa3x\xb6>\xdc\x83\x96\xd1\xf7\x92\xcf&W\xf4n\xc0\xd3\xc8\xfe\xd3\xfd"


class TestAirgapUpdateScreen(GraphicUnitTest):

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
    def test_init(self, mock_get_locale):
        screen = AirgapUpdateScreen()
        self.render(screen)

        self.assertEqual(screen.firmware_bin, "")
        self.assertEqual(screen.firmware_sig, "")

        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_firmware_bin(self, mock_get_locale):
        screen = AirgapUpdateScreen()
        screen.update(
            name=screen.name, key="binary", value=os.path.join("mock", "firmware.bin")
        )

        self.assertEqual(screen.firmware_bin, os.path.join("mock", "firmware.bin"))
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_firmware_sig(self, mock_get_locale):
        screen = AirgapUpdateScreen()
        screen.update(
            name=screen.name,
            key="signature",
            value=os.path.join("mock", "firmware.bin.sig"),
        )

        self.assertEqual(screen.firmware_sig, os.path.join("mock", "firmware.bin.sig"))
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_update_drives(self, mock_get_locale):
        screen = AirgapUpdateScreen()
        screen.update(name=screen.name, key="drives", value=[os.path.join("mock", "0")])

        self.assertTrue(f"{screen.id}_grid" in screen.ids)
        self.assertTrue(f"{screen.id}_button_0" in screen.ids)

        button_0_text = screen.ids[f"{screen.id}_button_0"].text
        self.assertEqual(
            button_0_text,
            "".join(
                [
                    "Select",
                    "\n",
                    f"[color=#efcc00]{os.path.join("mock", "0")}[/color]",
                    "\n",
                    "to copy firmware",
                ]
            ),
        )
        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    def test_on_leave(self, mock_get_locale):
        screen = AirgapUpdateScreen()
        screen.update(name=screen.name, key="drives", value=[os.path.join("mock", "0")])

        self.assertTrue(f"{screen.id}_grid" in screen.ids)
        self.assertTrue(f"{screen.id}_button_0" in screen.ids)

        # now clean
        screen.on_leave()
        self.assertTrue(f"{screen.id}_grid" not in screen.ids)

        mock_get_locale.assert_any_call()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.base_screen.BaseScreen.set_background")
    def test_on_press_button(self, mock_set_background, mock_get_locale):
        screen = AirgapUpdateScreen()
        screen.update(name=screen.name, key="drives", value=[os.path.join("mock", "0")])

        action = getattr(AirgapUpdateScreen, f"on_press_{screen.id}_button_0")
        action(screen.ids[f"{screen.id}_button_0"])

        mock_get_locale.assert_any_call()
        mock_set_background.assert_called_once_with(
            wid=f"{screen.id}_button_0", rgba=(0.25, 0.25, 0.25, 1)
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch(
        "src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US.UTF-8"
    )
    @patch("src.app.screens.airgap_update_screen.Clock.schedule_once")
    @patch("src.app.screens.airgap_update_screen.partial")
    @patch("src.app.screens.base_screen.BaseScreen.set_background")
    @patch("src.app.screens.base_screen.BaseScreen.set_screen")
    @patch("src.app.screens.airgap_update_screen.shutil.copyfile")
    @patch("src.utils.verifyer.sha256_verifyer.os.path.exists", return_value=True)
    @patch(
        "src.utils.verifyer.sha256_verifyer.open",
        new_callable=mock_open,
        read_data=MOCK_SIG,
    )
    def test_on_release_button(
        self,
        open_mock,
        mock_exists,
        mock_copyfile,
        mock_set_screen,
        mock_set_background,
        mock_partial,
        mock_schedule_once,
        mock_get_locale,
    ):
        screen = AirgapUpdateScreen()
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()

        screen.update(name=screen.name, key="drives", value=[os.path.join("mock", "0")])

        action = getattr(AirgapUpdateScreen, f"on_release_{screen.id}_button_0")
        action(screen.ids[f"{screen.id}_button_0"])

        mock_get_locale.assert_any_call()
        mock_partial.assert_called()
        mock_schedule_once.assert_called()
        mock_set_background.assert_called_once_with(
            wid=f"{screen.id}_button_0", rgba=(0, 0, 0, 1)
        )
        mock_set_screen.assert_called_once_with(
            name="WarningAfterAirgapUpdateScreen", direction="left"
        )
        mock_copyfile.assert_called()
        mock_exists.assert_called()
        open_mock.assert_called()

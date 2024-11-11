import sys
import importlib
import unittest
from unittest.mock import MagicMock, patch
from src.app.screens.base_screen import BaseScreen


class TestFailBaseScreenWindowsDrives(unittest.TestCase):

    def setUp(self):
        self.platform_patch = patch("sys.platform", "win32")
        self.platform_patch.start()
        self.mock_win32file = MagicMock()
        self.mock_win32file.GetLogicalDrives.side_effect = Exception("mock")

        with patch.dict("sys.modules", {"win32file": self.mock_win32file}):
            # Reload the base_screen module to apply the patch
            importlib.reload(sys.modules["src.app.screens.base_screen"])

    def tearDown(self):
        self.platform_patch.stop()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US")
    def test_fail_on_get_removable_drives_windows(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.redirect_exception = MagicMock()
        screen.on_get_removable_drives_windows()
        self.mock_win32file.GetLogicalDrives.assert_called_once()
        screen.redirect_exception.assert_called()
        mock_get_locale.assert_called_once()

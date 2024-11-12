import sys
import importlib
import unittest
from unittest.mock import MagicMock, patch
from src.app.screens.base_screen import BaseScreen


class TestBaseScreenWindowsDrives(unittest.TestCase):
    def setUp(self):
        # Patch `sys.platform` to simulate a Windows environment
        self.platform_patch = patch("sys.platform", "win32")
        self.platform_patch.start()
        self.mock_win32file = MagicMock()

        # Mock bitmask for drives D and E
        self.mock_win32file.GetLogicalDrives.return_value = 0b011000
        self.mock_win32file.DRIVE_REMOVABLE = 2  # Mock constant for removable drives
        self.mock_win32file.GetDriveType.side_effect = lambda drive: (
            self.mock_win32file.DRIVE_REMOVABLE if drive in ["D:\\", "E:\\"] else 3
        )

        with patch.dict("sys.modules", {"win32file": self.mock_win32file}):
            # Reload the base_screen module to apply the patch
            importlib.reload(sys.modules["src.app.screens.base_screen"])

    def tearDown(self):
        self.platform_patch.stop()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US")
    def test_on_get_removable_drives_windows(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.screen_manager = MagicMock()
        screen.screen_manager.get_screen = MagicMock()
        screen.on_get_removable_drives_windows()
        self.mock_win32file.GetLogicalDrives.assert_called_once()
        self.mock_win32file.GetDriveType.assert_any_call("D:\\")
        self.mock_win32file.GetDriveType.assert_any_call("E:\\")
        mock_get_locale.assert_called()

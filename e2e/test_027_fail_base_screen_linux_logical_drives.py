import sys
import importlib
import unittest
from unittest.mock import MagicMock, patch
from src.app.screens.base_screen import BaseScreen

MOCK_DISKS_LINUX = """
NAME="sda" TYPE="disk" RM="0" MOUNTPOINT=""
NAME="sda1" TYPE="part" RM="0" MOUNTPOINT="/boot"
NAME="sda2" TYPE="part" RM="0" MOUNTPOINT="/"
NAME="sda3" TYPE="part" RM="0" MOUNTPOINT="[SWAP]"
NAME="sdb" TYPE="disk" RM="1" MOUNTPOINT=""
NAME="sdb1" TYPE="part" RM="1" MOUNTPOINT="/media/mock/USB1"
NAME="sdc" TYPE="disk" RM="0" MOUNTPOINT=""
NAME="sdc1" TYPE="part" RM="0" MOUNTPOINT="/mnt/data"
NAME="sdd" TYPE="disk" RM="1" MOUNTPOINT=""
NAME="sdd1" TYPE="part" RM="1" MOUNTPOINT="/media/mock/USB2"
"""


# Mock named exception for this test
class CalledProcessError(Exception):

    def __init__(self, cmd, returncode):
        super().__init__(cmd)
        self.returncode = returncode


class TestBaseScreenLinuxDrives(unittest.TestCase):
    def setUp(self):
        self.platform_patch = patch("sys.platform", "linux")
        self.platform_patch.start()

        mock_run = MagicMock()
        mock_run.side_effect = CalledProcessError(cmd="mock", returncode=1)

        self.mock_subprocess = MagicMock()
        self.mock_subprocess.run = mock_run
        self.mock_subprocess.CalledProcessError = CalledProcessError

        with patch.dict("sys.modules", {"subprocess": self.mock_subprocess}):
            # Reload the base_screen module to apply the patch
            importlib.reload(sys.modules["src.app.screens.base_screen"])

    def tearDown(self):
        self.platform_patch.stop()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US")
    def test_on_get_removable_drives_windows(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.manager = MagicMock()
        screen.manager.get_screen = MagicMock()
        screen.redirect_exception = MagicMock()

        screen.on_get_removable_drives_linux()

        mock_get_locale.assert_called_once()
        self.mock_subprocess.run.assert_called_once_with(
            ["lsblk", "-P", "-o", "NAME,TYPE,RM,MOUNTPOINT"],
            capture_output=True,
            text=True,
            check=True,
        )
        screen.redirect_exception.assert_called()

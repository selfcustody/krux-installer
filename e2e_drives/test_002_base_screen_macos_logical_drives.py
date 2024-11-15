import sys
import importlib
import unittest
from unittest.mock import MagicMock, patch
from src.app.screens.base_screen import BaseScreen

MOCK_DISKS_MAC = """
   Device Identifier:        disk0
   Device Node:              /dev/disk0
   Whole:                    Yes
   Part of Whole:            disk0
   Device / Media Name:      Apple SSD
   Volume Name:              Macintosh HD
   Mounted:                  Yes
   Mount Point:              /
   File System:              APFS
   Content (IOContent):      Apple_APFS
   Device Block Size:        512 Bytes
   Disk Size:                500.3 GB (500279395328 Bytes)
   Read-Only Media:          No
   Removable Media:          No
   Solid State:              Yes
   Virtual:                  No
   Ejectable:                No

   Device Identifier:        disk0s1
   Device Node:              /dev/disk0s1
   Whole:                    No
   Part of Whole:            disk0
   Volume Name:              EFI
   Mounted:                  No
   File System:              MS-DOS (FAT32)
   Content (IOContent):      EFI
   Device Block Size:        512 Bytes
   Disk Size:                209.7 MB (209715200 Bytes)
   Read-Only Media:          No
   Removable Media:          No

   Device Identifier:        disk0s2
   Device Node:              /dev/disk0s2
   Whole:                    No
   Part of Whole:            disk0
   Volume Name:              Macintosh HD - Data
   Mounted:                  Yes
   Mount Point:              /System/Volumes/Data
   File System:              APFS
   Content (IOContent):      Apple_APFS
   Device Block Size:        512 Bytes
   Disk Size:                500.1 GB (500000000000 Bytes)
   Read-Only Media:          No
   Removable Media:          No

   Device Identifier:        disk1
   Device Node:              /dev/disk1
   Device Location:          External
   Whole:                    Yes
   Part of Whole:            disk1
   Device / Media Name:      External USB Drive
   Volume Name:              Backup Drive
   Mounted:                  Yes
   Mount Point:              /Volumes/Backup Drive
   File System:              FAT32
   File System Personality   MS-DOS FAT32
   Content (IOContent):      Apple_HFS
   Device Block Size:        4096 Bytes
   Disk Size:                2.0 TB (2000000000000 Bytes)
   Read-Only Media:          No
   Removable Media:          Yes
   Solid State:              No
   Virtual:                  No
   Ejectable:                Yes
"""


class TestBaseScreenLinuxDrives(unittest.TestCase):
    def setUp(self):
        self.platform_patch = patch("sys.platform", "darwin")
        self.platform_patch.start()

        mock_stdout = MagicMock(stdout=MOCK_DISKS_MAC)

        mock_run = MagicMock()
        mock_run.return_value = mock_stdout

        self.mock_subprocess = MagicMock()
        self.mock_subprocess.run = mock_run

        with patch.dict("sys.modules", {"subprocess": self.mock_subprocess}):
            # Reload the base_screen module to apply the patch
            importlib.reload(sys.modules["src.app.screens.base_screen"])

    def tearDown(self):
        self.platform_patch.stop()

    @patch("src.app.screens.base_screen.BaseScreen.get_locale", return_value="en_US")
    def test_on_get_removable_drives_mac(self, mock_get_locale):
        screen = BaseScreen(wid="mock", name="Mock")
        screen.screen_manager = MagicMock()
        screen.screen_manager.get_screen = MagicMock()

        disks = screen.on_get_removable_drives_macos()

        self.assertEqual(len(disks), 1)

        mock_get_locale.assert_called_once()
        self.mock_subprocess.run.assert_called_once_with(
            ["diskutil", "info", "-all"],
            capture_output=True,
            text=True,
            check=True,
        )

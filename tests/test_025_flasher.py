from unittest import TestCase
from unittest.mock import patch, call
from src.utils.flasher import Flasher
from .shared_mocks import MockListPorts, MockSerial


class TestFlasher(TestCase):

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_flash_linux(self, mock_process, mock_list_ports, mock_exists):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash()

        mock_exists.assert_has_calls(
            [
                call("mock/maixpy_test/kboot.kfpkg"),
                call("/mock/path"),
                call("/mock/path"),
            ]
        )

        mock_process.assert_called_once_with(
            terminal=False,
            dev="/mock/path",
            baudrate=1500000,
            board="dan",
            sram=False,
            file="mock/maixpy_test/kboot.kfpkg",
        )

    @patch("sys.platform", "linux")
    @patch("os.path.exists", return_value=False)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_fail_flash_linux_inexistent_firmware(
        self, mock_process, mock_list_ports, mock_exists
    ):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            f.flash()
        self.assertEqual(
            str(exc_info.exception), "File do not exist: mock/maixpy_test/kboot.kfpkg"
        )

    @patch("sys.platform", "win32")
    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.Serial", side_effect=MockSerial)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_flash_windows(
        self, mock_process, mock_list_ports, mock_serial, mock_exists
    ):
        f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
        f.flash()

        mock_exists.assert_called_once_with("mock/maixpy_test/kboot.kfpkg")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="COM1",
            baudrate=1500000,
            board="dan",
            sram=False,
            file="mock/maixpy_test/kboot.kfpkg",
        )

    @patch("sys.platform", "win32")
    @patch("os.path.exists", return_value=False)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_fail_flash_windows_inexistent_firmware(
        self, mock_process, mock_list_ports, mock_exists
    ):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            f.flash()
        self.assertEqual(
            str(exc_info.exception), "File do not exist: mock/maixpy_test/kboot.kfpkg"
        )

    @patch("sys.platform", "win32")
    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPorts)
    @patch("src.utils.kboot.build.ktool.KTool.process", side_effect=[True])
    # pylint: disable=unused-argument
    def test_fail_flash_windows_inexistent_port(
        self, mock_process, mock_list_ports, mock_exists
    ):
        msgs = [
            "[Errno 2] could not open port COM0: [Errno 2] No such file or directory: 'COM0'",
            "could not open port 'COM0': "
            + "FileNotFoundError(2, 'The system cannot find the file specified.', None, 2)",
        ]

        with self.assertRaises(RuntimeError) as exc_info:
            f = Flasher(firmware="mock/maixpy_test/kboot.kfpkg")
            f.flash()

        self.assertIn(str(exc_info.exception), msgs)

from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from src.utils.flasher import Flasher
from .shared_mocks import MockListPortsGrep


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_flash_success(
        self,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call(mock_next().device),
            ],
            any_order=True,
        )
        mock_process.assert_called_once_with(
            terminal=False,
            dev="mock",
            baudrate=1500000,
            board="goE",
            file="mock/maixpy_amigo/kboot.kfpkg",
            callback=callback,
        )

    @patch("os.path.exists", return_value=False)
    def test_fail_flash_firmware_not_exist(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher()
            f.firmware = "mock/maixpy_amigo/kboot.kfpkg"

        self.assertEqual(
            str(exc_info.exception),
            "File does not exist: mock/maixpy_amigo/kboot.kfpkg",
        )
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")

    @patch("os.path.exists", return_value=True)
    def test_fail_flash_wrong_baudrate(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher()
            f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
            f.baudrate = 1234567

        self.assertEqual(str(exc_info.exception), "Invalid baudrate: 1234567")
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_flash_after_first_greeting_fail(
        self,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_exception = Exception("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception, True]
        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            MagicMock(device="mocked_next")
        ]

        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call("mocked"),
                call("mocked_next"),
            ]
        )
        mock_process.assert_has_calls(
            [
                call(
                    terminal=False,
                    dev="mocked",
                    baudrate=1500000,
                    board="goE",
                    file="mock/maixpy_amigo/kboot.kfpkg",
                    callback=callback,
                ),
                call(
                    terminal=False,
                    dev="mocked_next",
                    baudrate=1500000,
                    board="goE",
                    file="mock/maixpy_amigo/kboot.kfpkg",
                    callback=callback,
                ),
            ]
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=False)
    @patch("src.utils.flasher.base_flasher.KTool.log")
    def test_fail_flash_port_not_working(
        self,
        mock_ktool_log,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()

        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call(mock_next().device),
            ],
            any_order=True,
        )
        mock_ktool_log.assert_called_once_with("Port mock not working")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch(
        "src.utils.flasher.flasher.Flasher.is_port_working", side_effect=[True, False]
    )
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.base_flasher.KTool.log")
    def test_fail_flash_after_first_greeting_fail_port_not_working(
        self,
        mock_ktool_log,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_exception = RuntimeError("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception]
        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            MagicMock(device="mocked_next")
        ]

        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls([call("mocked"), call("mocked_next")])
        mock_process.assert_has_calls(
            [
                call(
                    terminal=False,
                    dev="mocked",
                    baudrate=1500000,
                    board="goE",
                    file="mock/maixpy_amigo/kboot.kfpkg",
                    callback=callback,
                ),
            ]
        )
        mock_ktool_log.assert_has_calls([call("Port mocked_next not working")])

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch(
        "src.utils.flasher.flasher.Flasher.is_port_working", side_effect=[True, True]
    )
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.base_flasher.KTool.log")
    def test_fail_flash_after_first_greeting_fail_stop_iteration(
        self,
        mock_ktool_log,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_exception = Exception("Greeting fail: mock test")
        mock_process.side_effect = [mock_exception, True]

        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            StopIteration("mocked stop")
        ]

        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/maixpy_amigo/kboot.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/maixpy_amigo/kboot.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_next.assert_called_once()
        mock_is_port_working.assert_has_calls(
            [
                call("mocked"),
            ]
        )
        mock_process.assert_has_calls(
            [
                call(
                    terminal=False,
                    dev="mocked",
                    baudrate=1500000,
                    board="goE",
                    file="mock/maixpy_amigo/kboot.kfpkg",
                    callback=callback,
                ),
            ]
        )
        mock_ktool_log.assert_has_calls([call("mocked stop")])

from unittest import TestCase
from unittest.mock import patch, MagicMock, call
from src.utils.constants import FirmwareIntegrityError
from src.utils.flasher import Flasher
from .shared_mocks import MockListPortsGrep


class TestFlasher(TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_flash_success(
        self,
        mock_verify_firmware,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
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
            file="mock/firmware/amigo.kfpkg",
            callback=callback,
        )
        mock_verify_firmware.assert_called_once_with(
            "amigo", "mock/firmware/amigo.kfpkg"
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_flash_verifies_firmware_immediately_before_writing(
        self,
        mock_verify_firmware,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        # The window this closes is the one between MainScreen's check and
        # the write, so what matters is not only that the hash is checked
        # but that nothing happens between the check and KTool.process.
        order = []
        mock_verify_firmware.side_effect = lambda *args: order.append("verify")
        mock_process.side_effect = lambda **kwargs: order.append("process")

        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        self.assertEqual(order, ["verify", "process"])
        mock_verify_firmware.assert_called_once_with(
            "amigo", "mock/firmware/amigo.kfpkg"
        )
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_is_port_working.assert_has_calls([call(mock_next().device)])

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_fail_flash_tampered_firmware_is_never_written(
        self,
        mock_verify_firmware,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        mock_verify_firmware.side_effect = FirmwareIntegrityError("mocked tamper")
        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000

        with self.assertRaises(FirmwareIntegrityError) as exc_info:
            f.flash(callback=callback)

        # Nothing reached the device, and the failure was not swallowed by
        # the alternative-port retry, which would flash the same bad file
        self.assertEqual(str(exc_info.exception), "mocked tamper")
        mock_process.assert_not_called()
        mock_verify_firmware.assert_called_once_with(
            "amigo", "mock/firmware/amigo.kfpkg"
        )
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
        mock_list_ports.grep.assert_called_once_with("0403")
        mock_is_port_working.assert_called_once_with("mock")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_fail_flash_tampered_firmware_on_alternative_port(
        self,
        mock_verify_firmware,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        # The retry re-opens the file, so it re-hashes it too: a swap that
        # lands between the first attempt and the second is still caught
        mock_verify_firmware.side_effect = [None, FirmwareIntegrityError("mocked swap")]
        mock_process.side_effect = [Exception("Greeting fail: mock test")]
        mock_next.side_effect = [MagicMock(device="mocked")]
        mock_list_ports.grep.return_value.__next__.side_effect = [
            MagicMock(device="mocked_next")
        ]

        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000

        with self.assertRaises(FirmwareIntegrityError) as exc_info:
            f.flash(callback=callback)

        self.assertEqual(str(exc_info.exception), "mocked swap")
        self.assertEqual(mock_verify_firmware.call_count, 2)
        mock_process.assert_called_once()
        mock_is_port_working.assert_has_calls([call("mocked"), call("mocked_next")])
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_fail_flash_undetectable_device(
        self,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        # A file name that does not name a device leaves nothing to check the
        # firmware against: refuse rather than write something unverified
        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()
        f = Flasher()
        f.firmware = "mock/unknown/kboot.kfpkg"
        f.baudrate = 1500000

        with self.assertRaises(ValueError) as exc_info:
            f.flash(callback=callback)

        self.assertEqual(
            str(exc_info.exception),
            "Unknown device for firmware: mock/unknown/kboot.kfpkg",
        )
        mock_process.assert_not_called()
        mock_exists.assert_called_once_with("mock/unknown/kboot.kfpkg")

        # An unresolved device also means no port was ever looked up
        mock_list_ports.grep.assert_not_called()
        mock_is_port_working.assert_not_called()

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_flash_ignores_device_names_in_the_surrounding_path(
        self,
        mock_verify_firmware,
        mock_process,
        mock_is_port_working,
        mock_next,
        mock_list_ports,
        mock_exists,
    ):
        # 'rabbit' contains 'bit', which used to win over the device the user
        # actually selected because it comes first in VALID_DEVICES. Only the
        # file name may decide, or the wrong board is driven and the firmware
        # is hashed against another device's entry
        firmware = "/home/rabbit/_MEI42/src/utils/firmware/v26.08.0/yahboom.kfpkg"
        mock_next.return_value = MagicMock(device="mock")
        callback = MagicMock()
        f = Flasher()
        f.firmware = firmware
        f.baudrate = 1500000
        f.flash(callback=callback)

        self.assertEqual(f.board, "goE")
        mock_verify_firmware.assert_called_once_with("yahboom", firmware)

        # yahboom's vendor id, not the 0403 that matching 'bit' would give
        mock_list_ports.grep.assert_called_once_with("7523")
        mock_process.assert_called_once_with(
            terminal=False,
            dev="mock",
            baudrate=1500000,
            board="goE",
            file=firmware,
            callback=callback,
        )
        mock_is_port_working.assert_has_calls([call(mock_next().device)])
        mock_exists.assert_called_once_with(firmware)

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    def test_fail_flash_with_port_without_detected_device(
        self,
        mock_process,
        mock_exists,
    ):
        # Fail-closed guard: nothing may be written while the device, and so
        # the hash to check against, is still unknown
        f = Flasher()
        f.firmware = "mock/firmware/amigo.kfpkg"

        with self.assertRaises(FirmwareIntegrityError) as exc_info:
            # pylint: disable=protected-access
            f._flash_with_port("mock", MagicMock())

        self.assertEqual(
            str(exc_info.exception),
            "Could not tell which device 'mock/firmware/amigo.kfpkg' belongs to. "
            "Refusing to flash unverified firmware.",
        )
        mock_process.assert_not_called()
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")

    @patch("os.path.exists", return_value=False)
    def test_fail_flash_firmware_not_exist(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher()
            f.firmware = "mock/firmware/amigo.kfpkg"

        self.assertEqual(
            str(exc_info.exception),
            "File does not exist: mock/firmware/amigo.kfpkg",
        )
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")

    @patch("os.path.exists", return_value=True)
    def test_fail_flash_wrong_baudrate(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            f = Flasher()
            f.firmware = "mock/firmware/amigo.kfpkg"
            f.baudrate = 1234567

        self.assertEqual(str(exc_info.exception), "Invalid baudrate: 1234567")
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch("src.utils.flasher.flasher.Flasher.is_port_working", return_value=True)
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_flash_after_first_greeting_fail(
        self,
        mock_verify_firmware,
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
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
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
                    file="mock/firmware/amigo.kfpkg",
                    callback=callback,
                ),
                call(
                    terminal=False,
                    dev="mocked_next",
                    baudrate=1500000,
                    board="goE",
                    file="mock/firmware/amigo.kfpkg",
                    callback=callback,
                ),
            ]
        )

        # the retry re-opens the file, so it re-hashes it as well
        self.assertEqual(mock_verify_firmware.call_count, 2)

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
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
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
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_fail_flash_after_first_greeting_fail_port_not_working(
        self,
        mock_verify_firmware,
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
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
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
                    file="mock/firmware/amigo.kfpkg",
                    callback=callback,
                ),
            ]
        )
        mock_ktool_log.assert_has_calls([call("Port mocked_next not working")])
        mock_verify_firmware.assert_called_once_with(
            "amigo", "mock/firmware/amigo.kfpkg"
        )

    @patch("os.path.exists", return_value=True)
    @patch("src.utils.flasher.base_flasher.list_ports", new_callable=MockListPortsGrep)
    @patch("src.utils.flasher.base_flasher.next")
    @patch(
        "src.utils.flasher.flasher.Flasher.is_port_working", side_effect=[True, True]
    )
    @patch("src.utils.kboot.build.ktool.KTool.process")
    @patch("src.utils.flasher.base_flasher.KTool.log")
    @patch("src.utils.flasher.flasher.verify_firmware")
    def test_fail_flash_after_first_greeting_fail_stop_iteration(
        self,
        mock_verify_firmware,
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
        f.firmware = "mock/firmware/amigo.kfpkg"
        f.baudrate = 1500000
        f.flash(callback=callback)

        # patch assertions
        mock_exists.assert_called_once_with("mock/firmware/amigo.kfpkg")
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
                    file="mock/firmware/amigo.kfpkg",
                    callback=callback,
                ),
            ]
        )
        mock_ktool_log.assert_has_calls([call("mocked stop")])
        mock_verify_firmware.assert_called_once_with(
            "amigo", "mock/firmware/amigo.kfpkg"
        )

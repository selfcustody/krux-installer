from unittest import TestCase
from unittest.mock import patch, call
from src.utils.flasher.base_flasher import BaseFlasher
from .shared_mocks import PropertyInstanceMock


class TestBaseFlasher(TestCase):

    @patch("os.path.exists", side_effect=[True, True])
    @patch(
        "src.utils.flasher.base_flasher.BaseFlasher.device",
        new_callable=PropertyInstanceMock,
    )
    def test_init(self, mock_device, mock_exists):
        mock_device.return_value = "test"

        f = BaseFlasher(device="test", root_path="mock")

        mock_exists.assert_has_calls(
            [call("mock"), call("mock/maixpy_test/kboot.kfpkg")]
        )
        mock_device.assert_has_calls([call(f, "test"), call(f)])

    def test_fail_init_device(self):
        with self.assertRaises(ValueError) as exc_info:
            BaseFlasher(device="test", root_path="mock")

        self.assertEqual(str(exc_info.exception), "Invalid device: test")

    def test_init_fail_root_path(self):
        with self.assertRaises(ValueError) as exc_info:
            BaseFlasher(device="m5stickv", root_path="mock")

        self.assertEqual(str(exc_info.exception), "Directory mock do not exist")

    @patch("os.path.exists", side_effect=[True, False])
    def test_init_fail_full_path(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            BaseFlasher(device="m5stickv", root_path="mock")

        mock_exists.assert_has_calls(
            [call("mock"), call("mock/maixpy_m5stickv/kboot.kfpkg")]
        )
        self.assertEqual(
            str(exc_info.exception),
            "File mock/maixpy_m5stickv/kboot.kfpkg do not exist",
        )

    @patch("os.path.exists", side_effect=[True, True])
    def test_get_kboot(self, mock_exists):
        f = BaseFlasher(device="m5stickv", root_path="mock")

        mock_exists.assert_has_calls(
            [call("mock"), call("mock/maixpy_m5stickv/kboot.kfpkg")]
        )

        self.assertEqual(f.ktool.killProcess, False)
        self.assertEqual(f.ktool.loader, None)
        self.assertEqual(f.ktool.print_callback, None)

    @patch("os.path.exists", side_effect=[True, True])
    def test_get_buffer(self, mock_exists):
        f = BaseFlasher(device="m5stickv", root_path="mock")

        mock_exists.assert_has_calls(
            [call("mock"), call("mock/maixpy_m5stickv/kboot.kfpkg")]
        )

        self.assertEqual(f.buffer.readable(), True)

    @patch("os.path.exists", side_effect=[True, True])
    def test_has_admin_privileges(self, mock_exists):
        f = BaseFlasher(device="m5stickv", root_path="mock")

        mock_exists.assert_has_calls(
            [call("mock"), call("mock/maixpy_m5stickv/kboot.kfpkg")]
        )

        self.assertEqual(f.has_admin_privilege, False)

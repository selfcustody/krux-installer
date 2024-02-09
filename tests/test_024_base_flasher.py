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
    def test_init_device(self, mock_device, mock_exists):
        mock_device.return_value = "test"

        f = BaseFlasher(device="test", root_path="mock")

        mock_exists.assert_has_calls(
            [call("mock"), call("mock/maixpy_test/kboot.kfpkg")]
        )

        self.assertEqual(f.device, "test")
        mock_device.assert_has_calls([call(f, "test"), call(f)])

    @patch(
        "src.utils.flasher.base_flasher.BaseFlasher.root_path",
        new_callable=PropertyInstanceMock,
    )
    def test_init1_root_path(self, mock_root_path):
        mock_root_path.return_value = "mock"

        f = BaseFlasher(device="m5stickv", root_path="mock")

        self.assertEqual(f.root_path, "mock")
        mock_root_path.assert_has_calls([call(f, "mock"), call(f)])

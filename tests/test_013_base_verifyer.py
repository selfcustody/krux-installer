from unittest import TestCase
from unittest.mock import patch
from src.utils.verifyer.base_verifyer import BaseVerifyer
from .shared_mocks import PropertyInstanceMock


class TestBaseVerifyerDownloader(TestCase):

    @patch(
        "src.utils.verifyer.base_verifyer.BaseVerifyer.filename",
        new_callable=PropertyInstanceMock,
    )
    def test_init_filename_r(self, mock_filename):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="r")
        mock_filename.assert_called_once_with(b, "mockfile.txt")

    def test_get_filename_r(self):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="r")
        self.assertEqual(b.filename, "mockfile.txt")

    @patch(
        "src.utils.verifyer.base_verifyer.BaseVerifyer.read_mode",
        new_callable=PropertyInstanceMock,
    )
    def test_init_read_mode_r(self, mock_read_mode):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="r")
        mock_read_mode.assert_called_once_with(b, "r")

    @patch(
        "src.utils.verifyer.base_verifyer.BaseVerifyer.read_mode",
        new_callable=PropertyInstanceMock,
    )
    def test_init_read_mode_rb(self, mock_read_mode):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="rb")
        mock_read_mode.assert_called_once_with(b, "rb")

    def test_get_read_mode_r(self):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="r")
        self.assertEqual(b.read_mode, "r")

    def test_get_read_mode_rb(self):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="rb")
        self.assertEqual(b.read_mode, "rb")

    def test_fail_init_read_mode(self):
        with self.assertRaises(ValueError) as exc_info:
            BaseVerifyer(filename="mockfile.txt", read_mode="w")

        self.assertEqual(str(exc_info.exception), "Invalid read_mode: w")

    @patch(
        "src.utils.verifyer.base_verifyer.BaseVerifyer.data",
        new_callable=PropertyInstanceMock,
    )
    def test_init_data(self, mock_data):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="rb")
        mock_data.assert_called_once_with(b, None)

    def test_get_data(self):
        b = BaseVerifyer(filename="mockfile.txt", read_mode="rb")
        self.assertEqual(b.data, None)

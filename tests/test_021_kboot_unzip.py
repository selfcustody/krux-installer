import tempfile
from unittest import TestCase
from unittest.mock import patch, call
from src.utils.unzip.kboot_unzip import KbootUnzip


class TestKbootUnzip(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_init_m5stickv(self, mock_exists):
        unzip = KbootUnzip(filename="test.zip", device="m5stickv")
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("test/maixpy_m5stickv/kboot.kfpkg", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

    @patch("os.path.exists", return_value=True)
    def test_init_amigo_tft(self, mock_exists):
        unzip = KbootUnzip(filename="test.zip", device="amigo_tft")
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("test/maixpy_amigo_tft/kboot.kfpkg", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

    @patch("os.path.exists", return_value=True)
    def test_init_amigo_ips(self, mock_exists):
        unzip = KbootUnzip(filename="test.zip", device="amigo_ips")
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("test/maixpy_amigo_ips/kboot.kfpkg", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

    @patch("os.path.exists", return_value=True)
    def test_init_dock(self, mock_exists):
        unzip = KbootUnzip(filename="test.zip", device="dock")
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("test/maixpy_dock/kboot.kfpkg", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

    @patch("os.path.exists", return_value=True)
    def test_init_bit(self, mock_exists):
        unzip = KbootUnzip(filename="test.zip", device="bit")
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("test/maixpy_bit/kboot.kfpkg", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

    @patch("os.path.exists", return_value=True)
    def test_init_yahboom(self, mock_exists):
        unzip = KbootUnzip(filename="test.zip", device="yahboom")
        mock_exists.assert_has_calls([call("test.zip"), call(tempfile.gettempdir())])
        self.assertEqual(unzip.filename, "test.zip")
        self.assertIn("test/maixpy_yahboom/kboot.kfpkg", unzip.members)
        self.assertEqual(unzip.output, tempfile.gettempdir())

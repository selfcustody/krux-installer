import io
from unittest import TestCase
from unittest.mock import patch, mock_open
from src.utils.verifyer.check_verifyer import CheckVerifyer

mock_file = io.BytesIO()

# pylint: disable=line-too-long
mock_file.write(
    b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
)


class TestCheckVerifyerDownloader(TestCase):

    @patch("re.findall", return_value=["test.mock"])
    @patch("os.path.exists", return_value=True)
    def test_init(self, mock_exists, mock_findall):
        c = CheckVerifyer(filename="test.mock", read_mode="r", regexp=r".*mock")
        self.assertEqual(c.filename, "test.mock")
        mock_findall.assert_called_once_with(r".*mock", "test.mock")
        mock_exists.assert_called_once_with("test.mock")

    @patch("re.findall", return_value=[])
    def test_fail_init_re(self, mock_findall):
        with self.assertRaises(ValueError) as exc_info:
            CheckVerifyer(filename="test.mock", read_mode="r", regexp=r".*notmock")

        mock_findall.assert_called_once_with(r".*notmock", "test.mock")
        self.assertEqual(
            str(exc_info.exception),
            "Invalid file: test.mock do not assert with .*notmock",
        )

    @patch("os.path.exists", return_value=False)
    def test_fail_init_exists(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            CheckVerifyer(filename="test.mock", read_mode="r", regexp=r".*\.mock")

        mock_exists.assert_called_once_with("test.mock")
        self.assertEqual(str(exc_info.exception), "File test.mock do not exist")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="Hello World!")
    def test_load_r(self, open_mock, mock_exists):
        c = CheckVerifyer(filename="test.mock", read_mode="r", regexp=r".*\.mock")
        c.load()
        mock_exists.assert_called_once_with("test.mock")
        open_mock.assert_called_once_with("test.mock", "r", encoding="utf8")
        self.assertEqual(c.data, "Hello World!")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=mock_file.read())
    def test_load_rb(self, open_mock, mock_exists):
        c = CheckVerifyer(filename="test.mock", read_mode="rb", regexp=r".*\.mock")
        c.load()
        mock_exists.assert_called_once_with("test.mock")
        open_mock.assert_called_once_with("test.mock", "rb")
        self.assertIsInstance(c.data, bytes)

from unittest import TestCase
from unittest.mock import patch, mock_open
from src.utils.verifyer.pem_check_verifyer import PemCheckVerifyer

MOCK_PEM = """-----BEGIN PUBLIC KEY-----
MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgADM56IMVfkWJHmHKnfTNO7iV7zLUdbjnk1
WeoQo2dmaJs=
-----END PUBLIC KEY-----"""


class TestPemCheckVerifyerDownloader(TestCase):

    @patch("os.path.exists", return_value=True)
    def test_init(self, mock_exists):
        p = PemCheckVerifyer(filename="test.mock.pem")
        self.assertEqual(p.filename, "test.mock.pem")
        self.assertEqual(p.read_mode, "rb")
        mock_exists.assert_called_once_with("test.mock.pem")

    @patch("os.path.exists", return_value=True)
    def test_fail_init(self, mock_exists):
        with self.assertRaises(ValueError) as exc_info:
            PemCheckVerifyer(filename="test.mock.txt")
            mock_exists.assert_called_once_with("test.mock.txt")

        self.assertEqual(
            str(exc_info.exception),
            "Invalid file: test.mock.txt do not assert with .*\\.pem",
        )

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data=MOCK_PEM)
    def test_load(self, open_mock, mock_exists):
        p = PemCheckVerifyer(filename="test.mock.pem")
        p.load()
        mock_exists.assert_called_once_with("test.mock.pem")
        open_mock.assert_called_once_with("test.mock.pem", "rb")
        self.assertEqual(
            p.data,
            """-----BEGIN PUBLIC KEY-----
MDYwEAYHKoZIzj0CAQYFK4EEAAoDIgADM56IMVfkWJHmHKnfTNO7iV7zLUdbjnk1
WeoQo2dmaJs=
-----END PUBLIC KEY-----""",
        )

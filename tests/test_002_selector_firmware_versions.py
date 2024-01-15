from unittest import TestCase
from unittest.mock import patch, MagicMock
import requests
from src.utils.selector import (
    get_releases,
    get_releases_by_key,
    set_firmware_version,
    get_firmware_version,
)

MOCKED_EMPTY_API = []
MOCKED_FOUND_API = [
    {"tag_name": "v0.0.1"},
    {"tag_name": "v0.1.0"},
    {"tag_name": "v1.0.0"},
]


class TestSelectorFirmwareVersions(TestCase):
    @patch("src.utils.selector.requests")
    def test_success_request_get_releases(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API

        mock_requests.get.return_value = mock_response

        data = get_releases()
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], {"tag_name": "v0.0.1"})
        self.assertEqual(data[1], {"tag_name": "v0.1.0"})
        self.assertEqual(data[2], {"tag_name": "v1.0.0"})

    @patch("src.utils.selector.requests")
    def test_client_fail_request_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            get_releases()

        self.assertEqual(str(exc_info.exception), "HTTP error 404: None")

    @patch("src.utils.selector.requests")
    def test_server_fail_response_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            get_releases()

        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")

    @patch("src.utils.selector.requests")
    def test_fail_timeout_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            get_releases()

        self.assertEqual(str(exc_info.exception), "Timeout error: None")

    @patch("src.utils.selector.requests")
    def test_fail_connection_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError()
        )

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            get_releases()

        self.assertEqual(str(exc_info.exception), "Connection error: None")

    @patch("src.utils.selector.requests")
    def test_get_releases_by_key_tag_name(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API

        mock_requests.get.return_value = mock_response

        data = get_releases()
        tags = get_releases_by_key(data, "tag_name")

        self.assertEqual(type(tags[0]), str)
        self.assertEqual(type(tags[1]), str)
        self.assertEqual(type(tags[2]), str)
        self.assertEqual(tags[0], "v0.0.1")
        self.assertEqual(tags[1], "v0.1.0")
        self.assertEqual(tags[2], "v1.0.0")

    @patch("src.utils.selector.requests")
    def test_get_empty_releases_by_key_tag_name(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_EMPTY_API

        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            data = get_releases()
            get_releases_by_key(data, "tag_name")

        self.assertEqual(str(exc_info.exception), "Empty list")

    @patch("src.utils.selector.requests")
    def test_fail_get_releases_by_key_tag_name(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API

        mock_requests.get.return_value = mock_response

        with self.assertRaises(KeyError) as exc_info:
            data = get_releases()
            get_releases_by_key(data, "invalid_key")

        self.assertEqual(str(exc_info.exception), "'invalid_key'")

    @patch("src.utils.selector.requests")
    def test_set_firmware_version(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = MOCKED_FOUND_API

        mock_requests.get.return_value = mock_response

        with patch("src.utils.selector.Cache.append") as mock_cache_append:
            set_firmware_version("v0.0.1")
            mock_cache_append.assert_called_once_with(
                "krux-installer", "firmware-version", "v0.0.1"
            )

    @patch("src.utils.selector.requests")
    def test_fail_set_firmware_version(self, mock_requests):
        mock_response = MagicMock(status_code=200)
        mock_response.json.return_value = MOCKED_FOUND_API

        mock_requests.get.return_value = mock_response

        with patch("src.utils.selector.Cache.append") as mock_cache_append:
            with self.assertRaises(ValueError) as exc_info:
                set_firmware_version("v1.2.3")
                mock_cache_append.assert_called_once_with(
                    "krux-installer", "firmware-version", "v0.0.1"
                )
            self.assertEqual(str(exc_info.exception), "Firmware 'v1.2.3' is not valid")

    @patch("src.utils.selector.Cache.get", return_value="v0.0.1")
    def test_get_firmware_version(self, mock_cache_get):
        fw_version = get_firmware_version()
        mock_cache_get.assert_called_once()
        self.assertEqual(fw_version, "v0.0.1")

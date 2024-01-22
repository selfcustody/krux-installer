from unittest import TestCase
from unittest.mock import patch, MagicMock, call
import requests
from src.utils.selector import Selector

MOCKED_EMPTY_API = []
MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v0.0.1"},
    {"author": "test", "tag_name": "v0.1.0"},
    {"author": "test", "tag_name": "v1.0.0"},
]
MOCKED_TAGS = ["v0.0.1", "v0.1.0", "v1.0.0"]


class TestSelectorFirmwareVersions(TestCase):
    @patch("src.utils.selector.requests")
    def test_requests_on_get_releases(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.get_releases()

        mock_requests.get.assert_called_once_with(
            url="https://api.github.com/repos/selfcustody/krux/releases",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
        )

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.requests")
    def test_logger_on_get_releases(self, mock_requests, mock_debug):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        selector.get_releases()

        mock_debug.assert_has_calls(
            [
                call(
                    "get_releases::URL=https://api.github.com/repos/selfcustody/krux/releases"
                ),
                call("get_releases::HEADER=Accept: application/vnd.github+json"),
                call("get_releases::HEADER=X-Github-Api-Version: 2022-11-28"),
                call(f"get_releases::response='{MOCKED_FOUND_API}'"),
            ]
        )

    @patch("src.utils.selector.requests")
    def test_client_fail_request_get_releases(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            selector = Selector()
            selector.get_releases()

        self.assertEqual(str(exc_info.exception), "HTTP error 404: None")

    @patch("src.utils.selector.requests")
    def test_server_fail_response_get_releases(self, mock_requests):
        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            selector = Selector()
            selector.get_releases()

        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")

    @patch("src.utils.selector.requests")
    def test_fail_timeout_get_releases(self, mock_requests):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            selector = Selector()
            selector.get_releases()

        self.assertEqual(str(exc_info.exception), "Timeout error: None")

    @patch("src.utils.selector.requests")
    def test_fail_connection_get_releases(self, mock_requests):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError()
        )
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            selector = Selector()
            selector.get_releases()

        self.assertEqual(str(exc_info.exception), "Connection error: None")

    @patch("src.utils.selector.Selector.get_releases")
    def test_get_releases_by_key_tag_name(self, mock_get_releases):
        mock_get_releases.return_value = MOCKED_FOUND_API

        selector = Selector()
        selector.get_releases_by_key("tag_name")

        mock_get_releases.assert_called_once()

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Selector.get_releases")
    def test_logger_get_releases_by_key_tag_name(self, mock_get_releases, mock_debug):
        mock_get_releases.return_value = MOCKED_FOUND_API

        selector = Selector()
        selector.get_releases_by_key("tag_name")

        mock_debug.assert_has_calls(
            [
                call("get_releases_by_key::key=tag_name"),
                call("get_releases_by_key::value=['v0.0.1', 'v0.1.0', 'v1.0.0']"),
            ]
        )

    @patch("src.utils.selector.Selector.get_releases")
    def test_fail_get_releases_key_tag_name_valueerror(self, mock_get_releases):
        mock_get_releases.return_value = MOCKED_EMPTY_API

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.get_releases_by_key("tag_name")

        self.assertEqual(str(exc_info.exception), "Empty data")

    @patch("src.utils.selector.Selector.get_releases")
    def test_fail_get_releases_key_tag_name_keyerror(self, mock_get_releases):
        mock_get_releases.return_value = MOCKED_FOUND_API

        with self.assertRaises(KeyError) as exc_info:
            selector = Selector()
            selector.get_releases_by_key("test")

        self.assertEqual(str(exc_info.exception), "'Invalid key: test'")

    @patch("src.utils.selector.Cache.append")
    @patch("src.utils.selector.Selector.get_releases_by_key")
    def test_cache_append_set_firmware_version(
        self, mock_get_releases_by_key, mock_cache_append
    ):
        mock_get_releases_by_key.return_value = MOCKED_TAGS

        selector = Selector()
        selector.set_firmware_version("v0.0.1")

        mock_cache_append.assert_called_once_with(
            "krux-installer", "firmware-version", "v0.0.1"
        )

    @patch("src.utils.selector.Selector.get_releases_by_key")
    def test_fail_set_firmware_version(self, mock_get_releases_by_key):
        mock_get_releases_by_key.append.side_effect = ValueError

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.set_firmware_version("v1.2.3")

        self.assertEqual(str(exc_info.exception), "Firmware 'v1.2.3' is not valid")

    @patch("src.utils.selector.Cache.get", return_value="v0.0.1")
    def test_get_firmware_version(self, mock_cache_get):
        selector = Selector()
        fw_version = selector.get_firmware_version()
        mock_cache_get.assert_called_once()
        self.assertEqual(fw_version, "v0.0.1")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Selector.get_releases_by_key")
    def test_logger_set_firmware_version(self, mock_get_releases_by_key, mock_debug):
        mock_get_releases_by_key.return_value = MOCKED_TAGS

        selector = Selector()
        selector.set_firmware_version("v0.0.1")

        mock_debug.assert_has_calls(
            [
                call("set_firmware_version::append=odudex/krux_binaries"),
                call("cache::append::krux-installer::firmware-version=v0.0.1"),
            ]
        )

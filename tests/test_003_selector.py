from unittest import TestCase
from unittest.mock import MagicMock, patch
import requests
from src.utils.selector import Selector


MOCKED_EMPTY_API = []
MOCKED_WRONG_API = [
    {"author": "test"},
    {"author": "test"},
    {"author": "test"},
]
MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v0.0.1"},
    {"author": "test", "tag_name": "v0.1.0"},
    {"author": "test", "tag_name": "v1.0.0"},
]


class TestSelector(TestCase):

    @patch("src.utils.selector.requests")
    def test_init(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()

        mock_requests.get.assert_called_once_with(
            url="https://api.github.com/repos/selfcustody/krux/releases",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
        )

        self.assertEqual(selector.releases[0], "v0.0.1")
        self.assertEqual(selector.releases[1], "v0.1.0")
        self.assertEqual(selector.releases[2], "v1.0.0")

    @patch("src.utils.selector.requests")
    def test_fail_init_empty_data(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_EMPTY_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            Selector()

        self.assertEqual(
            str(exc_info.exception),
            "https://api.github.com/repos/selfcustody/krux/releases returned empty data",
        )

    @patch("src.utils.selector.requests")
    def test_fail_init_wrong_data(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_WRONG_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(KeyError) as exc_info:
            Selector()

        self.assertEqual(
            str(exc_info.exception), "\"Invalid key: 'tag_name' do not exist on api\""
        )

    @patch("src.utils.selector.requests")
    def test_fail_init_http_error_404(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "HTTP error 404: None")

    @patch("src.utils.selector.requests")
    def test_fail_init_http_error_500(self, mock_requests):
        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")

    @patch("src.utils.selector.requests")
    def test_fail_init_timeout(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "Timeout error: None")

    @patch("src.utils.selector.requests")
    def test_fail_init_http_connection_error(self, mock_requests):
        mock_response = MagicMock(status_code=404)
        mock_response.raise_for_status.side_effect = requests.exceptions.ConnectionError
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "Connection error: None")

    @patch("src.utils.selector.requests")
    def test_set_get_device(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()

        for device in ("m5stickv", "amigo", "dock", "bit", "yahboom", "cube"):
            selector.device = device
            self.assertEqual(selector.device, device)

    @patch("src.utils.selector.requests")
    def test_fail_set_device(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.device = "mock"

        self.assertEqual(str(exc_info.exception), "Device 'mock' is not valid")

    @patch("src.utils.selector.requests")
    def test_set_get_firmware(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        selector = Selector()
        for version in ("v0.0.1", "v0.1.0", "v1.0.0"):
            selector.firmware = version
            self.assertTrue(selector.firmware in ("v0.0.1", "v0.1.0", "v1.0.0"))

    @patch("src.utils.selector.requests")
    def test_fail_set_firmware(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.firmware = "v0.0.111"

        self.assertEqual(str(exc_info.exception), "Firmware 'v0.0.111' is not valid")

from unittest import TestCase
from unittest.mock import patch, MagicMock
import pytest
import requests
from src.utils.selector import get_releases, list_by_key

MOCKED_API_JSON = [
    {"tag_name": "v0.0.1"},
    {"tag_name": "v0.1.0"},
    {"tag_name": "v1.0.0"},
]


class TestSelectorFirmwareVersions(TestCase):
    @patch("src.utils.selector.requests")
    def test_success_request_get_releases(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_API_JSON

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

        with pytest.raises(RuntimeError) as exc_info:
            get_releases()

        assert str(exc_info.value) == "HTTP error 404: None"

    @patch("src.utils.selector.requests")
    def test_server_fail_response_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_requests.get.return_value = mock_response

        with pytest.raises(RuntimeError) as exc_info:
            get_releases()

        assert str(exc_info.value) == "HTTP error 500: None"

    @patch("src.utils.selector.requests")
    def test_fail_timeout_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mock_requests.get.return_value = mock_response

        with pytest.raises(RuntimeError) as exc_info:
            get_releases()

        assert str(exc_info.value) == "Timeout error: None"

    @patch("src.utils.selector.requests")
    def test_fail_connection_get_releases(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError()
        )

        mock_requests.get.return_value = mock_response

        with pytest.raises(RuntimeError) as exc_info:
            get_releases()

        assert str(exc_info.value) == "Connection error: None"

    @patch("src.utils.selector.requests")
    def test_list_by_key_tag_name(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_API_JSON

        mock_requests.get.return_value = mock_response

        data = get_releases()
        tags = list_by_key(data, "tag_name")

        self.assertEqual(type(tags[0]), str)
        self.assertEqual(type(tags[1]), str)
        self.assertEqual(type(tags[2]), str)
        self.assertEqual(tags[0], "v0.0.1")
        self.assertEqual(tags[1], "v0.1.0")
        self.assertEqual(tags[2], "v1.0.0")

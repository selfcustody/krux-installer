from unittest import TestCase
from unittest.mock import patch
from src.utils.selector import (
    request_krux_releases,
    get_releases_tags,
)

MOCKED_API_JSON = """[
    {"tag_name": "v0.0.1"},
    {"tag_name": "v0.1.0"},
    {"tag_name": "v1.0.0"}
]
"""


class TestSelectorFirmwareVersions(TestCase):
    # pylint: disable=unused-argument
    @patch("src.utils.selector.urlopen")
    def test_request_krux_releases(self, mock_urlopen):
        request_krux_releases()
        self.assertEqual(mock_urlopen.call_count, 1)

    @patch("src.utils.selector.HTTPResponse.read")
    def test_get_releases_tags(self, mock_read):
        mock_read.return_value = MOCKED_API_JSON

        response = request_krux_releases()
        tags = get_releases_tags(response)
        self.assertEqual(mock_read.call_count, 1)
        self.assertEqual(len(tags), 3)
        self.assertEqual(tags[0], "v0.0.1")
        self.assertEqual(tags[1], "v0.1.0")
        self.assertEqual(tags[2], "v1.0.0")

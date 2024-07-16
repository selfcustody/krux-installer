import io
from unittest import TestCase
from unittest.mock import patch, MagicMock, call
import requests
from src.utils.downloader.stream_downloader import StreamDownloader
from .shared_mocks import PropertyInstanceMock

URL = "https://github.com/selfcustody/krux"

MOCKED_FOUND_API = [
    {"author": "test", "tag_name": "v0.0.1"},
    {"author": "test", "tag_name": "v0.1.0"},
    {"author": "test", "tag_name": "v1.0.0"},
]


class TestStreamDownloader(TestCase):

    @patch(
        "src.utils.downloader.asset_downloader.StreamDownloader.on_data",
        new_callable=PropertyInstanceMock,
    )
    def test_init_on_data(self, mock_on_data):
        # fake a zip file to be downloaded
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # mock a stream of bytes from fake zipfile
        stream = [
            [bytes(b) for b in file.read(i + 7)] for i in range(file.__sizeof__())
        ]
        s = StreamDownloader(url=URL)
        s.on_data = mock_on_data

        calls = []
        for chunk in stream:
            s.downloaded_len += len(chunk)
            s.on_data(data=chunk)
            calls.append(call()(data=[]))

        mock_on_data.assert_has_calls(calls, any_order=True)

    @patch("src.utils.downloader.stream_downloader.requests")
    def test_download_file_stream(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = MOCKED_FOUND_API
        mock_requests.get.return_value = mock_response

        sd = StreamDownloader(url=URL)
        sd.download_file_stream(url="https://any.call/test.zip")

        mock_requests.get.assert_called_once_with(
            url="https://any.call/test.zip",
            stream=True,
            headers={
                "Content-Disposition": "attachment filename=test.zip",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept-Encoding": "gzip, deflate, br",
            },
            timeout=30,
        )
        mock_requests.get.return_value.iter_content.assert_called_with(chunk_size=1024)

    @patch("src.utils.downloader.stream_downloader.requests")
    def test_server_fail_download_file_stream(self, mock_requests):
        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            sd = StreamDownloader(url=URL)
            sd.download_file_stream(url="https://any.request/test.zip")

        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")

    @patch("src.utils.downloader.stream_downloader.requests")
    def test_fail_timeout_download_file_stream(self, mock_requests):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            sd = StreamDownloader(url=URL)
            sd.download_file_stream(url="https://any.request/test.zip")

        self.assertEqual(str(exc_info.exception), "Download timeout error: None")

    @patch("src.utils.downloader.stream_downloader.requests")
    def test_fail_connection_download_file_stream(self, mock_requests):
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError()
        )
        mock_requests.exceptions = requests.exceptions
        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            sd = StreamDownloader(url=URL)
            sd.download_file_stream(url="https://any.request/test.zip")

        self.assertEqual(str(exc_info.exception), "Download connection error: None")

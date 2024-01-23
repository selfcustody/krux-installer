import io
import tempfile
from unittest import TestCase
from unittest.mock import patch, MagicMock, call
import requests
from src.utils.downloader import StreamDownloaderZipRelease


class TestDownloader(TestCase):
    @patch("src.utils.downloader.StreamDownloaderZipRelease.debug")
    def test_debug_init(self, mock_debug):
        tmp = tempfile.gettempdir()
        StreamDownloaderZipRelease(version="v0.0.1")
        url = "https://github.com/selfcustody/krux/releases/download/v0.0.1/krux-v0.0.1.zip"
        mock_debug.assert_has_calls(
            [
                call("set_on_data::on_data"),
                call(f"set_destdir::destdir={tmp}"),
                call(f"set_url::url={url}"),
                call("set_on_data::on_data"),
            ]
        )

    @patch("src.utils.downloader.StreamDownloaderZipRelease.debug")
    @patch("src.utils.downloader.requests")
    def test_download(self, mock_requests, mock_debug):
        # fake a zip file to be downloaded
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200

        # mock a stream of bytes from fake zipfile
        mock_response.iter_content.return_value = [
            [bytes(b) for b in file.read(i + 7)] for i in range(file.__sizeof__())
        ]
        mock_requests.get.return_value = mock_response

        # mock the on_data callback
        mock_on_data = MagicMock()

        sd = StreamDownloaderZipRelease(version="v0.0.1")
        sd.set_on_data(callback=mock_on_data)
        sd.download()

        mock_requests.get.assert_called_once_with(
            url="https://github.com/selfcustody/krux/releases/download/v0.0.1/krux-v0.0.1.zip",
            stream=True,
            headers={
                "Content-Disposition": "attachment filename=krux-v0.0.1.zip",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept-Encoding": "gzip, deflate, br",
            },
            timeout=30,
        )

        tmp = str(tempfile.gettempdir())
        mock_requests.get.return_value.iter_content.assert_called_with(chunk_size=1024)
        mock_on_data.assert_called()
        mock_debug.assert_any_call("set_on_data::on_data")
        mock_debug.assert_any_call(f"set_destdir::destdir={tmp}")
        mock_debug.assert_any_call(
            "set_url::url=https://github.com/selfcustody/krux/releases/download/v0.0.1/krux-v0.0.1.zip"
        )
        mock_debug.assert_any_call(f"download::destfile={tmp}/krux-v0.0.1.zip")
        mock_debug.assert_any_call("download_file_stream::filename=krux-v0.0.1.zip")
        mock_debug.assert_any_call(
            "download_file_stream::requests.get=< url: https://github.com/selfcustody/krux/releases/download/v0.0.1/krux-v0.0.1.zip, stream: True, headers: {'Content-Disposition': 'attachment filename=krux-v0.0.1.zip', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Accept-Encoding': 'gzip, deflate, br'}, timeout: 30 >"
        )
        mock_debug.assert_any_call("download_file_stream::raise_for_status")
        mock_debug.assert_any_call("download_file_stream::content_len=1")
        mock_debug.assert_any_call("download_file_stream::downloaded_len=0")
        mock_debug.assert_any_call("downloaded_file_stream::closing_connection")
        mock_debug.assert_any_call("download::destfile=/tmp/krux-v0.0.1.zip")
        mock_debug.assert_any_call("download::zip_file.write=b''")

    @patch("src.utils.downloader.requests")
    def test_fail_download_on_data_not_set(self, mock_requests):
        # fake a zip file to be downloaded
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200

        # mock a stream of bytes from fake zipfile
        mock_response.iter_content.return_value = [
            [bytes(b) for b in file.read(i + 7)] for i in range(file.__sizeof__())
        ]
        mock_requests.get.return_value = mock_response

        with self.assertRaises(NotImplementedError) as exc_info:
            sd = StreamDownloaderZipRelease(version="v0.0.1")
            sd.set_on_write_to_buffer(callback=None)
            sd.download()

        self.assertEqual(
            str(exc_info.exception), "Use 'set_callback_on_write_to_buffer'"
        )

    @patch("src.utils.downloader.requests")
    def test_fail_notexist_download(self, mock_requests):
        mock_requests.exceptions = requests.exceptions
        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            mock_on_data = MagicMock()

            sd = StreamDownloaderZipRelease(version="v0.0.1")
            sd.set_on_data(callback=mock_on_data)
            sd.download()

        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")

    @patch("src.utils.downloader.requests")
    def test_fail_timeout_download(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            mock_on_data = MagicMock()

            sd = StreamDownloaderZipRelease(version="v0.0.1")
            sd.set_on_data(callback=mock_on_data)
            sd.download()

        self.assertEqual(str(exc_info.exception), "Timeout error: None")

    @patch("src.utils.downloader.requests")
    def test_fail_connection_download(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = (
            requests.exceptions.ConnectionError()
        )

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:
            mock_on_data = MagicMock()

            sd = StreamDownloaderZipRelease(version="v0.0.1")
            sd.set_on_data(callback=mock_on_data)
            sd.download()

        self.assertEqual(str(exc_info.exception), "Connection error: None")

    @patch("src.utils.downloader.requests")
    def test_write_to_buffer(self, mock_requests):
        # fake a zip file to be downloaded
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # mock a stream of bytes from fake zipfile
        stream = [bytes(file.read(i)) for i in range(file.__sizeof__())]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = stream
        mock_requests.get.return_value = mock_response

        mock_on_write = MagicMock()

        sd = StreamDownloaderZipRelease(version="v0.0.1")
        sd.set_on_write_to_buffer(callback=mock_on_write)
        sd.download()

        mock_on_write.assert_called()

    # @patch("src.utils.downloader.requests")
    # def test_write_to_buffer(self, mock_requests):
    #     # fake a zip file to be downloaded
    #     file = io.BytesIO()

    #     # pylint: disable=line-too-long
    #     file.write(
    #         b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
    #     )

    #     # mock the response
    #     mock_response = MagicMock()
    #     mock_response.status_code = 200

    #     # mock a stream of bytes from fake zipfile
    #     mock_response.iter_content.return_value = [
    #         [bytes(b) for b in file.read(i + 7)] for i in range(file.__sizeof__())
    #     ]

    #     mock_requests.get.return_value = mock_response

    #     # mock the on_data callback
    #     mock_on_data = MagicMock()
    #     mock_on_write_to_buffer = MagicMock()

    #     sd = StreamDownloaderZipRelease(version="v0.0.1")
    #     sd.set_on_data(callback=mock_on_data)
    #     sd.set_on_write_to_buffer(callback=mock_on_write_to_buffer)
    #     sd.download()

    #     mock_on_data.assert_called()
    #     mock_on_write_to_buffer.assert_called()

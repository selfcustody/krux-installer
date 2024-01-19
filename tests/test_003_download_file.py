import io
import os
from unittest import TestCase
from unittest.mock import patch, MagicMock, Mock
import requests
from src.utils.downloader import download_file_stream, progress_bar_cli

URL = "https://someurl.com/krux-v0.0.1.zip"

def foo(callback):
    callback('Buzz', 'Lightyear')

#--- pytest code ---

class TestDownloader(TestCase):
    
    @patch("src.utils.downloader.requests")
    def test_download_file_stream_with_default_chunk_size(self, mock_requests):
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
        mock_response.iter_content.return_value = [ [bytes(b) for b in file.read(i+7) ] for i in range(file.__sizeof__())]
        mock_requests.get.return_value = mock_response

        # mock the on_data callback
        mock_on_data = MagicMock()

        download_file_stream(url=URL, on_data=mock_on_data)
        mock_requests.get.assert_called_once_with(
            url="https://someurl.com/krux-v0.0.1.zip",
            stream=True,
            headers={
                "Content-Disposition": "attachment filename=krux-v0.0.1.zip",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept-Encoding": "gzip, deflate, br",
            },
            timeout=10,
        )
        mock_requests.get.return_value.iter_content.assert_called_with(chunk_size=1024)
        mock_on_data.assert_called()

    @patch("src.utils.downloader.requests")
    def test_download_file_stream_with_custom_chunk_size(self, mock_requests):
        
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
        mock_response.iter_content.return_value = [ [bytes(b) for b in file.read(i+7) ] for i in range(file.__sizeof__())]
        mock_requests.get.return_value = mock_response
        
        # mock the on_data callback
        mock_on_data = MagicMock()

        download_file_stream(url=URL, chunk_size=512, on_data=mock_on_data)
        mock_requests.get.assert_called_once_with(
            url="https://someurl.com/krux-v0.0.1.zip",
            stream=True,
            headers={
                "Content-Disposition": "attachment filename=krux-v0.0.1.zip",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "Accept-Encoding": "gzip, deflate, br",
            },
            timeout=10,
        )
        mock_requests.get.return_value.iter_content.assert_called_with(chunk_size=512)
        mock_on_data.assert_called()

    @patch("src.utils.downloader.requests")
    def test_fail_download_file_stream_with_default_chunk_size(self, mock_requests):
        mock_requests.exceptions = requests.exceptions
        mock_response = MagicMock(status_code=500)
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:

            def mock_on_data():
                pass

            download_file_stream(url=URL, on_data=mock_on_data)
        
        self.assertEqual(str(exc_info.exception), "HTTP error 500: None")


    @patch("src.utils.downloader.requests")
    def test_fail_timeout_download_file_stream(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.Timeout()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:

            def mock_on_data():
                pass

            download_file_stream(url=URL, on_data=mock_on_data)
        
        self.assertEqual(str(exc_info.exception), "Timeout error: None")

    @patch("src.utils.downloader.requests")
    def test_fail_connection_download_file_stream(self, mock_requests):
        mock_requests.exceptions = requests.exceptions

        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.ConnectionError()

        mock_requests.get.return_value = mock_response

        with self.assertRaises(RuntimeError) as exc_info:

            def mock_on_data():
                pass

            download_file_stream(url=URL, on_data=mock_on_data)
        
        self.assertEqual(str(exc_info.exception), "Connection error: None")

        
    @patch("src.utils.downloader.sys.stdout", new_callable=io.StringIO)
    def test_progress_bar_cli(self, mock_stdout):

        # mock sys.stdout.write function
        mock_stdout.write = MagicMock()

        # fake a zip file to be downloaded
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # mock a stream of bytes from fake zipfile
        stream = [ [bytes(b) for b in file.read(i+7) ] for i in range(file.__sizeof__())]

        # do same procedure from downloade_file_stream
        downloaded_len = 0
        for chunk in stream:
            downloaded_len += len(chunk)
            progress_bar_cli(
                data=chunk,
                content_len=file.getbuffer().nbytes,
                downloaded_len=downloaded_len,
                started_at=123.456
            )

        mock_stdout.write.assert_called()

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_print_progress_bar_cli(self, mock_print):

        # fake a zip file to be downloaded
        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        # mock a stream of bytes from fake zipfile
        stream = [ [bytes(b) for b in file.read(i+7) ] for i in range(file.__sizeof__())]

        # do same procedure from downloade_file_stream
        downloaded_len = 0
        for chunk in stream:
            downloaded_len += len(chunk)
            progress_bar_cli(
                data=chunk,
                content_len=file.getbuffer().nbytes,
                downloaded_len=downloaded_len,
                started_at=123.456
            )

        print_val = mock_print.getvalue()
        print_size = len(print_val)
        last_char = print_val[print_size - 1]
        self.assertEqual(last_char, "s")

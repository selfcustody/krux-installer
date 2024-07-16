import io
import sys
from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open
from src.utils.downloader.asset_downloader import AssetDownloader
from .shared_mocks import PropertyInstanceMock


class TestAssetDownloader(TestCase):

    @patch(
        "src.utils.downloader.asset_downloader.AssetDownloader.destdir",
        new_callable=PropertyInstanceMock,
    )
    @patch("tempfile.gettempdir")
    def test_init_destdir(self, mock_gettempdir, mock_destdir):
        mock_gettempdir.return_value = "/tmp/dir"

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.zip",
            destdir=mock_gettempdir(),
            write_mode="w",
        )

        mock_destdir.assert_called_once_with(a, "/tmp/dir")

    @patch(
        "src.utils.downloader.asset_downloader.AssetDownloader.write_mode",
        new_callable=PropertyInstanceMock,
    )
    @patch("tempfile.gettempdir")
    def test_init_write_mode(self, mock_gettempdir, mock_mode):
        mock_gettempdir.return_value = "/tmp/dir"

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.zip",
            destdir=mock_gettempdir(),
            write_mode="w",
        )

        mock_mode.assert_called_once_with(a, "w")

    @patch("tempfile.gettempdir")
    def test_fail_init_write_mode(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        with self.assertRaises(ValueError) as exc_info:
            AssetDownloader(
                url="https://github.com/selfcustody/krux/asset.zip",
                destdir=mock_gettempdir(),
                write_mode="r",
            )

        self.assertEqual(str(exc_info.exception), "Write Mode 'r' not supported")

    @patch("builtins.open", new_callable=mock_open)
    @patch("tempfile.gettempdir")
    @patch("src.utils.downloader.stream_downloader.requests")
    def test_download_wb(self, mock_requests, mock_gettempdir, open_mock):
        if sys.platform in ("linux", "darwin"):
            mock_gettempdir.return_value = "/tmp/dir"

        if sys.platform == "win32":
            mock_gettempdir.return_value = "C:\\tmp\\dir"

        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        stream = [bytes(b) for b in file.read(8)]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = stream
        mock_requests.get.return_value = mock_response

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.zip",
            destdir=mock_gettempdir(),
            write_mode="wb",
        )

        mock_on_data = MagicMock()
        a.download(on_data=mock_on_data)

        if sys.platform in ("linux", "darwin"):
            open_mock.assert_called_once_with("/tmp/dir/asset.zip", "wb")

        if sys.platform == "win32":
            open_mock.assert_called_once_with("C:\\tmp\\dir\\asset.zip", "wb")

    @patch("builtins.open", new_callable=mock_open)
    @patch("tempfile.gettempdir")
    @patch("src.utils.downloader.stream_downloader.requests")
    def test_download_w(self, mock_requests, mock_gettempdir, open_mock):
        if sys.platform in ("linux", "darwin"):
            mock_gettempdir.return_value = "/tmp/dir"

        if sys.platform == "win32":
            mock_gettempdir.return_value = "C:\\tmp\\dir"

        file = io.BytesIO()

        # pylint: disable=line-too-long
        file.write(
            b"PK\x03\x04\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x1c\x00tests/krux.txtUT\t\x00\x03\x7f\xeb\xa7e\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00\xad\x90K\x0e\xc2 \x14E\xe7\xae\x82\r\x94~\x8c\x03;s%\rE\xa8/\x94O(m\xd1\xd5k\xd5\xc4X\x13\x05\xe2\xf8\xdd\x93s\xf2\x0e\x96\x9e`b5B\xc2\x8e>\x9b\xaa-.\xf6\xb8\xc4\x170\x1b\x84@\xf1\x9e8P]\xfd~\xce\x85\xd3\xba\xcfzP\xa3G\xe8\xf7P\x12\x1a8\xcb\xca\"d9\x83\xc2\xcc\xb3\xefSI\xc0\x9bs#w\x83\x03*\xa6\x9c\x83\x953\xb1\x0c\xb77z\x80.\x9d\x8e#E\xab\xb5\xc3\x82\x1b\x11\xa6$\x12:\xdd\x80\x19\xe2\x9d/\xf4?\xd2\xe07=p\xc7]j\xf3\x82\xa65\xaf\xa5\xc1\xcd-$\xd4.Pl\xe7Z\x14\\x\xd4T\xc4'\xde\xa9\xd8\xc6\x0f\xd53\xf2\nPK\x01\x02\x1e\x03\x14\x00\x00\x00\x08\x00\x08`1Xb\x1f\x95Q\xb3\x00\x00\x00!\x04\x00\x00\x0e\x00\x18\x00\x00\x00\x00\x00\x01\x00\x00\x00\xa4\x81\x00\x00\x00\x00tests/krux.txtUT\x05\x00\x03\x7f\xeb\xa7eux\x0b\x00\x01\x04\xe8\x03\x00\x00\x04\xe8\x03\x00\x00PK\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00T\x00\x00\x00\xfb\x00\x00\x00\x00\x00"
        )

        stream = [bytes(b) for b in file.read(8)]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = stream
        mock_requests.get.return_value = mock_response

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.txt",
            destdir=mock_gettempdir(),
            write_mode="w",
        )

        mock_on_data = MagicMock()
        a.download(on_data=mock_on_data)

        if sys.platform in ("linux", "darwin"):
            open_mock.assert_called_once_with(
                "/tmp/dir/asset.txt", "w", encoding="utf8"
            )

        if sys.platform == "win32":
            open_mock.assert_called_once_with(
                "C:\\tmp\\dir\\asset.txt", "w", encoding="utf8"
            )

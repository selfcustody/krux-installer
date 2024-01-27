from unittest import TestCase
from unittest.mock import patch, call
from src.utils.downloader.asset_downloader import AssetDownloader
from .property_instance_mock import PropertyInstanceMock


class TestAssetDownloader(TestCase):
    @patch("tempfile.gettempdir")
    def test_fail_init(self, mock_gettempdir):
        mock_gettempdir.return_value = "/tmp/dir"

        with self.assertRaises(ValueError) as exc_info:
            AssetDownloader(
                url="https://some.url/asset.zip",
                destdir=mock_gettempdir(),
                write_mode="w",
            )
        self.assertEqual(
            str(exc_info.exception), "Invalid url: https://some.url/asset.zip"
        )

    @patch(
        "src.utils.downloader.asset_downloader.AssetDownloader.url",
        new_callable=PropertyInstanceMock,
    )
    @patch("tempfile.gettempdir")
    def test_init_url(self, mock_gettempdir, mock_url):
        mock_gettempdir.return_value = "/tmp/dir"

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.zip",
            destdir=mock_gettempdir(),
            write_mode="w",
        )

        mock_url.assert_called_once_with(
            a, "https://github.com/selfcustody/krux/asset.zip"
        )

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

    @patch(
        "src.utils.downloader.asset_downloader.AssetDownloader.on_data",
        new_callable=PropertyInstanceMock,
    )
    @patch("tempfile.gettempdir")
    def test_init_on_data(self, mock_gettempdir, mock_on_data):
        mock_gettempdir.return_value = "/tmp/dir"

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.zip",
            destdir=mock_gettempdir(),
            write_mode="w",
        )

        calls = [call(a, a.progress_bar_cli), call(a, a.write_to_buffer)]
        mock_on_data.assert_has_calls(calls)

    @patch(
        "src.utils.downloader.asset_downloader.AssetDownloader.on_write_to_buffer",
        new_callable=PropertyInstanceMock,
    )
    @patch("tempfile.gettempdir")
    def test_init_on_write_to_buffer(self, mock_gettempdir, mock_on_write):
        mock_gettempdir.return_value = "/tmp/dir"

        a = AssetDownloader(
            url="https://github.com/selfcustody/krux/asset.zip",
            destdir=mock_gettempdir(),
            write_mode="w",
        )

        mock_on_write.assert_called_once_with(a, a.progress_bar_cli)

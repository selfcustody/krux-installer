import os
from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from kivy.logger import LOG_LEVELS
from src.utils.selector import Selector


class TestSelector(TestCase):
    @patch.dict(os.environ, {"LOGLEVEL": "info"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_info(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Selector()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["info"])

    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_debug(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Selector()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["debug"])

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.append")
    def test_set_device_m5stickv_loglevel_info(self, mock_append, mock_debug):
        selector = Selector()
        selector.set_device("m5stickv")

        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::set::krux-installer::device=m5stickv"),
            ]
        )
        mock_append.assert_called_once_with("krux-installer", "device", "m5stickv")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.append")
    def test_set_device_amigo_tft_loglevel_info(self, mock_append, mock_debug):
        selector = Selector()
        selector.set_device("amigo_tft")

        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::set::krux-installer::device=amigo_tft"),
            ]
        )
        mock_append.assert_called_once_with("krux-installer", "device", "amigo_tft")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.append")
    def test_set_device_amigo_ips_loglevel_info(self, mock_append, mock_debug):
        selector = Selector()
        selector.set_device("amigo_ips")

        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::set::krux-installer::device=amigo_ips"),
            ]
        )
        mock_append.assert_called_once_with("krux-installer", "device", "amigo_ips")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.append")
    def test_set_device_dock_loglevel_info(self, mock_append, mock_debug):
        selector = Selector()
        selector.set_device("dock")

        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::set::krux-installer::device=dock"),
            ]
        )
        mock_append.assert_called_once_with("krux-installer", "device", "dock")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.append")
    def test_set_device_bit_loglevel_info(self, mock_append, mock_debug):
        selector = Selector()
        selector.set_device("bit")
        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::set::krux-installer::device=bit"),
            ]
        )
        mock_append.assert_called_once_with("krux-installer", "device", "bit")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.append")
    def test_set_device_yahboom_loglevel_info(self, mock_append, mock_debug):
        selector = Selector()
        selector.set_device("yahboom")
        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::set::krux-installer::device=yahboom"),
            ]
        )
        mock_append.assert_called_once_with("krux-installer", "device", "yahboom")

    @patch("src.utils.selector.Cache.append")
    def test_cache_raise_value_error(self, mock_append):
        mock_append.side_effect = ValueError
        with self.assertRaises(ValueError) as exc_info:
            selector = Selector()
            selector.set_device("lilygo")

        self.assertEqual(str(exc_info.exception), "Device 'lilygo' is not valid")

    @patch("src.utils.selector.Selector.debug")
    @patch("src.utils.selector.Cache.get", return_value="None")
    def test_cache_get_device(self, mock_get, mock_debug):
        selector = Selector()
        selector.get_device()

        mock_debug.assert_has_calls(
            [
                call("cache::register::krux-installer={limit: 10, timeout: 60}"),
                call("cache::get::krux-installer::device=None"),
            ]
        )

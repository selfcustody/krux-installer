import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
from kivy.logger import LOG_LEVELS
from src.utils.trigger import Trigger


class TestTrigger(TestCase):
    @patch.dict(os.environ, {"LOGLEVEL": "info"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_info(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Trigger()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["info"])

    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_debug(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Trigger()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["debug"])

    @patch.dict(os.environ, {"LOGLEVEL": "warning"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_warning(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Trigger()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["warning"])

    @patch.dict(os.environ, {"LOGLEVEL": "error"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_error(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Trigger()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["error"])

    @patch.dict(os.environ, {"LOGLEVEL": "lol"}, clear=True)
    def test_fail_init_loglevel_lol(self):
        with self.assertRaises(KeyError) as exc_info:
            Trigger()

        self.assertEqual(str(exc_info.exception), "'Not recognized LOGLEVEL: lol'")

    @patch("src.utils.trigger.inspect")
    def test_mro_info(self, mock_inspect):
        mock_f_code = MagicMock()
        mock_f_code.co_varnames = ["test.test_000_trigger.TestTrigger"]

        mock_f_back = MagicMock()
        mock_f_back.f_code = mock_f_code

        mock_inspect.currentframe.return_value = mock_f_back

        mro = Trigger.mro_info()
        mock_inspect.currentframe.assert_called_once()
        self.assertEqual(mro, None)

    @patch("src.utils.trigger.Trigger.mro_info", return_value="TestTrigger")
    def test_create_msg_loglevel_info(self, mock_mro_info):
        # pylint: disable=protected-access
        msg = Trigger._create_msg("Hello World")
        mock_mro_info.assert_called_once()
        self.assertEqual(msg, "TestTrigger: Hello World")

    @patch.dict(os.environ, {"LOGLEVEL": "info"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_info_method(self, mock_logger):
        trigger = Trigger()
        trigger.info("Hello World")
        mock_logger.info.assert_called_once_with("None: Hello World")

    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_debug_method(self, mock_logger):
        trigger = Trigger()
        trigger.debug("Hello World")
        mock_logger.debug.assert_called_once_with("None: Hello World")

    @patch.dict(os.environ, {"LOGLEVEL": "warning"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_warning_method(self, mock_logger):
        trigger = Trigger()
        trigger.warning("Hello World")
        mock_logger.warning.assert_called_once_with("None: Hello World")

    @patch.dict(os.environ, {"LOGLEVEL": "warning"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_error_method(self, mock_logger):
        trigger = Trigger()
        trigger.error("Hello World")
        mock_logger.error.assert_called_once_with("None: Hello World")

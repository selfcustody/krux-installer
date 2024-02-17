import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.utils.trigger import Trigger


class TestTrigger(TestCase):

    @patch("src.utils.trigger.currentframe")
    def test_mro_info(self, mock_currentframe):
        mock_f_code = MagicMock()
        mock_f_code.co_varnames = ["test.test_000_trigger.TestTrigger"]

        mock_f_back = MagicMock()
        mock_f_back.f_code = mock_f_code

        mock_currentframe.return_value = mock_f_back

        mro = Trigger.mro_info()
        mock_currentframe.assert_called_once()
        self.assertEqual(mro, None)

    @patch("src.utils.trigger.Trigger.mro_info", return_value="TestTrigger")
    def test_create_msg(self, mock_mro_info):
        # pylint: disable=protected-access
        msg = Trigger.create_msg("Hello World")
        mock_mro_info.assert_called_once()
        self.assertEqual(msg, "[TestTrigger]: Hello World")

    @patch.dict(os.environ, {"LOGLEVEL": "info"}, clear=True)
    @patch("builtins.print")
    def test_info_method(self, mock_print):
        trigger = Trigger()
        trigger.info("Hello World")
        mock_print.assert_called_once_with("[INFO ] [None]: Hello World")

    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("builtins.print")
    def test_debug_method(self, mock_print):
        trigger = Trigger()
        trigger.debug("Hello World")
        mock_print.assert_called_once_with("[DEBUG] [None]: Hello World")

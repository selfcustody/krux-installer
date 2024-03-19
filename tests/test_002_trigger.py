import os
from unittest import TestCase
from unittest.mock import patch
from src.utils.trigger import Trigger


class TestTrigger(TestCase):

    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_create_msg(self, mock_mro):
        t = Trigger()
        msg = t.create_msg("Hello World")
        mock_mro.assert_called_once()
        self.assertEqual(msg, "[Mock]: Hello World")

    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_info(self, mock_mro):
        t = Trigger()
        t.info("Hello World")
        mock_mro.assert_called_once()

    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_debug(self, mock_mro):
        trigger = Trigger()
        trigger.debug("Hello World")
        mock_mro.assert_called_once()

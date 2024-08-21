import os
from unittest import TestCase
from unittest.mock import patch
from src.utils.trigger import Trigger


class TestTrigger(TestCase):

    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_info(self, mock_mro):
        t = Trigger()
        t.info("Hello World")
        mock_mro.assert_called_once()

    @patch.dict(os.environ, {"LOGLEVEL": "warning"}, clear=True)
    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_warn(self, mock_mro):
        trigger = Trigger()
        trigger.warning("Hello World")
        mock_mro.assert_called_once()

    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_debug(self, mock_mro):
        trigger = Trigger()
        trigger.debug("Hello World")
        mock_mro.assert_called_once()

    @patch.dict(os.environ, {"LOGLEVEL": "critical"}, clear=True)
    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_critical(self, mock_mro):
        trigger = Trigger()
        trigger.critical("Hello World")
        mock_mro.assert_called_once()

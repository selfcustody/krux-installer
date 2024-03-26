import os
from unittest import TestCase
from unittest.mock import patch
from src.utils.trigger import Trigger


class TestTrigger(TestCase):

    @patch.dict(os.environ, {"LOGLEVEL": "info"}, clear=True)
    def test_init_info(self):
        t = Trigger()
        self.assertEqual(t.loglevel, "info")

    @patch.dict(os.environ, {"LOGLEVEL": "warn"}, clear=True)
    def test_init_warn(self):
        t = Trigger()
        self.assertEqual(t.loglevel, "warn")
        
    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    def test_init_error(self):
        t = Trigger()
        self.assertEqual(t.loglevel, "debug")
        
    @patch.dict(os.environ, {"LOGLEVEL": "mock"}, clear=True)
    def test_fail_init(self):
        with self.assertRaises(ValueError) as exc_info:
            Trigger()
        
        self.assertEqual(str(exc_info.exception), "Invalid loglevel: mock")
        
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

    @patch.dict(os.environ, {"LOGLEVEL": "warn"}, clear=True)
    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_warn(self, mock_mro):
        trigger = Trigger()
        trigger.warn("Hello World")
        mock_mro.assert_called_once()
        
    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.utils.trigger.mro", return_value="Mock")
    def test_debug(self, mock_mro):
        trigger = Trigger()
        trigger.debug("Hello World")
        mock_mro.assert_called_once()

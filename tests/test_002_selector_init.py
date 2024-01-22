import os
from unittest import TestCase
from unittest.mock import MagicMock, patch
from kivy.logger import LOG_LEVELS
from src.utils.selector import Selector


class TestSelectorInit(TestCase):
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

    @patch.dict(os.environ, {"LOGLEVEL": "warning"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_warning(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Selector()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["warning"])

    @patch.dict(os.environ, {"LOGLEVEL": "error"}, clear=True)
    @patch("src.utils.trigger.Logger")
    def test_init_loglevel_error(self, mock_logger):
        mock_set_level = MagicMock()
        mock_logger.setLevel = mock_set_level

        Selector()
        mock_logger.setLevel.assert_called_once_with(LOG_LEVELS["error"])

    @patch.dict(os.environ, {"LOGLEVEL": "lol"}, clear=True)
    def test_fail_init_loglevel_lol(self):
        with self.assertRaises(KeyError) as exc_info:
            Selector()

        self.assertEqual(str(exc_info.exception), "'Not recognized LOGLEVEL: lol'")

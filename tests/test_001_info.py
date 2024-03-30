from unittest import TestCase
from unittest.mock import MagicMock, patch
from src.utils.info import mro


class TestInfo(TestCase):

    @patch("src.utils.info.currentframe")
    def test_fail_co_varnames(self, mock_currentframe):
        mock_f_code = MagicMock()
        mock_f_code.co_varnames = []

        mock_f_back = MagicMock()
        mock_f_back.f_code = mock_f_code

        mock_currentframe.return_value = mock_f_back

        m = mro()
        mock_currentframe.assert_called_once()
        self.assertEqual(m, None)

    @patch("src.utils.info.currentframe")
    def test_fail_f_locals(self, mock_currentframe):
        mock_f_locals = MagicMock()
        mock_f_locals.side_effect = KeyError

        mock_f_code = MagicMock()
        mock_f_code.co_varnames = ["mock"]

        mock_f_back = MagicMock()
        mock_f_back.f_code = mock_f_code

        mock_currentframe.return_value = mock_f_back

        m = mro()
        mock_currentframe.assert_called_once()
        self.assertEqual(m, None)

    @patch("src.utils.info.currentframe")
    def test_empty_cls(self, mock_currentframe):
        mock_f_locals = MagicMock()
        mock_f_locals.return_value = {"mock": "test"}

        mock_f_code = MagicMock()
        mock_f_code.co_varnames = ["mock"]

        mock_f_back = MagicMock()
        mock_f_back.f_code = mock_f_code

        mock_currentframe.return_value = mock_f_back

        m = mro()
        mock_currentframe.assert_called_once()
        self.assertEqual(m, None)

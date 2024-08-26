import os
from unittest.mock import patch
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.base_krux_installer import BaseKruxInstaller


class TestBaseKruxInstaller(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("src.app.base_krux_installer.Logger.setLevel")
    def test_init(self, mock_set_level):
        app = BaseKruxInstaller()

        self.assertEqual(len(app.screens), 0)
        self.assertFalse(app.screen_manager is None)

        mock_set_level.assert_called_once_with(20)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LOGLEVEL": "debug"}, clear=True)
    @patch("src.app.base_krux_installer.Logger.setLevel")
    def test_init_debug(self, mock_set_level):

        app = BaseKruxInstaller()

        self.assertEqual(len(app.screens), 0)
        self.assertFalse(app.screen_manager is None)

        mock_set_level.assert_called_once_with(10)

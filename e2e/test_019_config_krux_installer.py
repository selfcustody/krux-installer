import os
from unittest.mock import patch, MagicMock, call, mock_open
from kivy.base import EventLoop, EventLoopBase
from kivy.tests.common import GraphicUnitTest
from src.app.config_krux_installer import ConfigKruxInstaller


class TestConfigKruxInstaller(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "linux")
    def test_get_system_lang_linux(self):
        lang = ConfigKruxInstaller.get_system_lang()
        self.assertEqual(lang, "en-US.UTF-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "darwin")
    def test_get_system_lang_darwin(self):
        lang = ConfigKruxInstaller.get_system_lang()
        self.assertEqual(lang, "en-US.UTF-8")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.ctypes")
    @patch("src.app.config_krux_installer.locale")
    def test_get_system_lang_win32(self, mock_locale, mock_ctypes):
        mock_ctypes = MagicMock()
        mock_ctypes.windll = MagicMock
        mock_ctypes.windll.kernel32 = MagicMock()
        mock_ctypes.windll.kernel32.GetUserDefaultUILanguage = MagicMock(
            return_value="en"
        )

        mock_locale = MagicMock()
        mock_locale.windows_locale = {"en": "en-US.UTF-8"}

        ConfigKruxInstaller.get_system_lang()

        mock_ctypes.windll.kernel32.GetUserDefaultUILanguage.assert_called_once()

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "mockos")
    def test_fail_get_system_lang(self):
        with self.assertRaises(OSError) as exc_info:
            ConfigKruxInstaller.get_system_lang()

        self.assertEqual(str(exc_info.exception), "OS 'mockos' not recognized")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    def test_get_app_dir_config_linux(self, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.get_app_dir(name="config")

        self.assertEqual(_dir, os.path.join("mockdir", ".config", "krux-installer"))

        # patch assertions
        mock_expanduser.assert_called_once_with("~")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.getenv", return_value="mockdir")
    def test_get_app_dir_config_win32(self, mock_getenv):
        app = ConfigKruxInstaller()
        _dir = app.get_app_dir(name="config")

        self.assertEqual(_dir, os.path.join("mockdir", "krux-installer", "config"))

        # patch assertions
        mock_getenv.assert_called_once_with("LOCALAPPDATA")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    def test_get_app_dir_config_darwin(self, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.get_app_dir(name="config")

        self.assertEqual(
            _dir,
            os.path.join(
                "mockdir", "Library", "Application Support", "krux-installer", "config"
            ),
        )

        # patch assertions
        mock_expanduser.assert_called_once_with("~")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "mockos")
    def test_fail_get_app_dir_config_wrong_name(self):
        app = ConfigKruxInstaller()

        with self.assertRaises(ValueError) as exc_info:
            app.get_app_dir(name="mock")

        self.assertEqual(str(exc_info.exception), "Invalid name: 'mock'")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "mockos")
    def test_fail_get_app_dir_config_wrong_os(self):
        app = ConfigKruxInstaller()

        with self.assertRaises(OSError) as exc_info:
            app.get_app_dir(name="config")

        self.assertEqual(str(exc_info.exception), "Not supported: mockos")

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_create_app_dir_linux(self, mock_makedirs, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", ".config", "krux-installer")

        self.assertEqual(_dir, dir_test)
        # patch assertions
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(dir_test)
        mock_makedirs.assert_called_once_with(dir_test)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.getenv", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_create_app_dir_win32(self, mock_makedirs, mock_exists, mock_getenv):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", "krux-installer", "config")

        self.assertEqual(_dir, dir_test)
        # patch assertions
        mock_getenv.assert_called_once_with("LOCALAPPDATA")
        mock_exists.assert_called_once_with(dir_test)
        mock_makedirs.assert_called_once_with(dir_test)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_create_app_dir_darwin(self, mock_makedirs, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join(
            "mockdir", "Library", "Application Support", "krux-installer", "config"
        )

        self.assertEqual(_dir, dir_test)
        # patch assertions
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(dir_test)
        mock_makedirs.assert_called_once_with(dir_test)

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_linux(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", ".config", "krux-installer", "config.ini")

        self.assertEqual(file, file_test)

        # patch assertions
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(file_test)
        open_mock.assert_has_calls(
            [
                call(file_test, "w", encoding="utf8"),
                call().write("# Generated config. Do not edit this manually!\n"),
            ],
            any_order=True,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.getenv", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_win32(self, open_mock, mock_exists, mock_getenv):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", "krux-installer", "config", "config.ini")

        self.assertEqual(file, file_test)

        # patch assertions
        mock_getenv.assert_called_once_with("LOCALAPPDATA")
        mock_exists.assert_called_once_with(file_test)
        open_mock.assert_has_calls(
            [
                call(file_test, "w", encoding="utf8"),
                call().write("# Generated config. Do not edit this manually!\n"),
            ],
            any_order=True,
        )

    @patch.object(EventLoopBase, "ensure_window", lambda x: None)
    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_darwin(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join(
            "mockdir",
            "Library",
            "Application Support",
            "krux-installer",
            "config",
            "config.ini",
        )

        self.assertEqual(file, file_test)

        # patch assertions
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(file_test)
        open_mock.assert_has_calls(
            [
                call(file_test, "w", encoding="utf8"),
                call().write("# Generated config. Do not edit this manually!\n"),
            ],
            any_order=True,
        )

import json
import os
import sys
from unittest.mock import MagicMock, call, mock_open, patch

from kivy.base import EventLoop
from kivy.clock import Clock
from kivy.tests.common import GraphicUnitTest

from src.app.config_krux_installer import ConfigKruxInstaller


class TestConfigKruxInstaller(GraphicUnitTest):
    @classmethod
    def teardown_class(cls):
        for event in Clock.get_events():
            Clock.unschedule(event)
        EventLoop.exit()

    @patch("src.app.config_krux_installer.LabelBase.register")
    @patch(
        "src.app.config_krux_installer.os.path.abspath",
        side_effect=[
            os.path.join("mock", "path", "assets"),
            os.path.join("mock", "path", "i18n"),
        ],
    )
    def test_init(self, mock_abspath, mock_register):
        with patch.dict(sys.__dict__, {"frozen": False}):
            ConfigKruxInstaller()
            mock_register.assert_called_once_with(
                "Roboto",
                os.path.join(
                    "mock", "path", "assets", "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
                ),
            )
            mock_abspath.assert_called()

    @patch("src.app.config_krux_installer.kv_resources.resource_add_path")
    @patch("src.app.config_krux_installer.LabelBase.register")
    def test_init_frozen_branch(self, mock_register, mock_resource_add_path):
        with patch.dict(
            sys.__dict__, {"_MEIPASS": os.path.join("mocked", "path"), "frozen": True}
        ):
            installer = ConfigKruxInstaller()
            mock_resource_add_path.assert_called_with(os.path.join("mocked", "path"))
            mock_register.assert_called_once_with(
                "Roboto",
                os.path.join(
                    "mocked", "path", "assets", "NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
                ),
            )
            self.assertEqual(
                installer.assets_path, os.path.join("mocked", "path", "assets")
            )
            self.assertEqual(
                installer.i18n_path, os.path.join("mocked", "path", "src", "i18n")
            )

    @patch("sys.platform", "linux")
    def test_make_lang_code_posix(self):
        lang = ConfigKruxInstaller.make_lang_code(lang="en_US")
        self.assertEqual(lang, "en_US.UTF-8")

    @patch("sys.platform", "win32")
    def test_make_lang_code_windows(self):
        lang = ConfigKruxInstaller.make_lang_code(lang="en_US")
        self.assertEqual(lang, "en_US")

    @patch("sys.platform", "mockos")
    def test_fail_make_lang_code(self):
        with self.assertRaises(OSError) as exc:
            ConfigKruxInstaller.make_lang_code(lang="en_US")
        self.assertEqual(
            str(exc.exception),
            "Couldn't possible to setup locale: OS 'mockos' not implemented",
        )

    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "linux")
    def test_get_system_lang_linux(self):
        lang = ConfigKruxInstaller.get_system_lang()
        self.assertEqual(lang, "en-US.UTF-8")

    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "darwin")
    def test_get_system_lang_darwin(self):
        lang = ConfigKruxInstaller.get_system_lang()
        self.assertEqual(lang, "en-US.UTF-8")

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

    @patch.dict(os.environ, {"LANG": "en-US.UTF-8"}, clear=True)
    @patch("sys.platform", "mockos")
    def test_fail_get_system_lang(self):
        with self.assertRaises(OSError) as exc_info:
            ConfigKruxInstaller.get_system_lang()

        self.assertEqual(str(exc_info.exception), "OS 'mockos' not recognized")

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    def test_get_app_dir_config_linux(self, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.get_app_dir(name="config")

        self.assertEqual(_dir, os.path.join("mockdir", ".config", "krux-installer"))
        mock_expanduser.assert_called_once_with("~")

    @patch.dict(os.environ, {"LOCALAPPDATA": "mockdir"}, clear=True)
    @patch("sys.platform", "win32")
    def test_get_app_dir_config_win32(self):
        app = ConfigKruxInstaller()
        _dir = app.get_app_dir(name="config")

        self.assertEqual(_dir, os.path.join("mockdir", "krux-installer", "config"))

    @patch.dict(os.environ, {"LOCALAPPDATA": ""}, clear=True)
    @patch("sys.platform", "win32")
    def test_fail_get_app_dir_config_win32_empty(self):
        app = ConfigKruxInstaller()
        with self.assertRaises(EnvironmentError) as exc_info:
            app.get_app_dir(name="config")

        self.assertEqual(str(exc_info.exception), "LOCALAPPDATA is empty")

    @patch.dict(os.environ, {"MOCKAPPDATA": "mockdir"}, clear=True)
    @patch("sys.platform", "win32")
    def test_fail_get_app_dir_config_win32_not_found(self):
        app = ConfigKruxInstaller()
        with self.assertRaises(EnvironmentError) as exc_info:
            app.get_app_dir(name="config")

        self.assertEqual(
            str(exc_info.exception), "LOCALAPPDATA environment variable not found"
        )

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    def test_get_app_dir_config_darwin(self, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.get_app_dir(name="config")

        self.assertEqual(_dir, os.path.join("mockdir", ".config", "krux-installer"))
        mock_expanduser.assert_called_once_with("~")

    @patch("sys.platform", "mockos")
    def test_fail_get_app_dir_config_wrong_name(self):
        app = ConfigKruxInstaller()

        with self.assertRaises(ValueError) as exc_info:
            app.get_app_dir(name="mock")

        self.assertEqual(str(exc_info.exception), "Invalid name: 'mock'")

    @patch("sys.platform", "mockos")
    def test_fail_get_app_dir_config_wrong_os(self):
        app = ConfigKruxInstaller()

        with self.assertRaises(OSError) as exc_info:
            app.get_app_dir(name="config")

        self.assertEqual(str(exc_info.exception), "Not supported: mockos")

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_create_app_dir_linux(self, mock_makedirs, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", ".config", "krux-installer")

        self.assertEqual(_dir, dir_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(dir_test)
        mock_makedirs.assert_called_once_with(dir_test)

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_skip_create_app_dir_linux(
        self, mock_makedirs, mock_exists, mock_expanduser
    ):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", ".config", "krux-installer")

        self.assertEqual(_dir, dir_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(dir_test)
        assert len(mock_makedirs.mock_calls) == 0

    @patch.dict(os.environ, {"LOCALAPPDATA": "mockdir"}, clear=True)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_create_app_dir_win32(self, mock_makedirs, mock_exists):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", "krux-installer", "config")

        self.assertEqual(_dir, dir_test)
        mock_exists.assert_called_once_with(dir_test)
        mock_makedirs.assert_called_once_with(dir_test)

    @patch.dict(os.environ, {"LOCALAPPDATA": "mockdir"}, clear=True)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_skip_create_app_dir_win32(self, mock_makedirs, mock_exists):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", "krux-installer", "config")

        self.assertEqual(_dir, dir_test)
        mock_exists.assert_called_once_with(dir_test)
        assert len(mock_makedirs.mock_calls) == 0

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_create_app_dir_darwin(self, mock_makedirs, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", ".config", "krux-installer")

        self.assertEqual(_dir, dir_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(dir_test)
        mock_makedirs.assert_called_once_with(dir_test)

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True])
    @patch("src.app.config_krux_installer.os.makedirs")
    def test_skip_create_app_dir_darwin(
        self, mock_makedirs, mock_exists, mock_expanduser
    ):
        app = ConfigKruxInstaller()
        _dir = app.create_app_dir(name="config")
        dir_test = os.path.join("mockdir", ".config", "krux-installer")

        self.assertEqual(_dir, dir_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(dir_test)
        assert len(mock_makedirs.mock_calls) == 0

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_linux(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", ".config", "krux-installer", "config.ini")

        self.assertEqual(file, file_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(file_test)
        open_mock.assert_has_calls(
            [
                call(file_test, "w", encoding="utf8"),
                call().write("# Generated config. Do not edit this manually!\n"),
            ],
            any_order=True,
        )

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True, True])
    @patch("builtins.open", new_callable=mock_open)
    def test_skip_create_app_file_linux(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", ".config", "krux-installer", "config.ini")

        self.assertEqual(file, file_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(file_test)
        assert len(open_mock.mock_calls) == 0

    @patch.dict(os.environ, {"LOCALAPPDATA": "mockdir"}, clear=True)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_win32(self, open_mock, mock_exists):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", "krux-installer", "config", "config.ini")

        self.assertEqual(file, file_test)
        mock_exists.assert_called_once_with(file_test)
        open_mock.assert_has_calls(
            [
                call(file_test, "w", encoding="utf8"),
                call().write("# Generated config. Do not edit this manually!\n"),
            ],
            any_order=True,
        )

    @patch.dict(os.environ, {"LOCALAPPDATA": "mockdir"}, clear=True)
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True, True])
    @patch("builtins.open", new_callable=mock_open)
    def test_skip_create_app_file_win32(self, open_mock, mock_exists):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", "krux-installer", "config", "config.ini")

        self.assertEqual(file, file_test)
        mock_exists.assert_called_once_with(file_test)
        assert len(open_mock.mock_calls) == 0

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_darwin(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", ".config", "krux-installer", "config.ini")

        self.assertEqual(file, file_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(file_test)
        open_mock.assert_has_calls(
            [
                call(file_test, "w", encoding="utf8"),
                call().write("# Generated config. Do not edit this manually!\n"),
            ],
            any_order=True,
        )

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True, True])
    @patch("builtins.open", new_callable=mock_open)
    def test_skip_create_app_file_darwin(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", ".config", "krux-installer", "config.ini")

        self.assertEqual(file, file_test)
        mock_expanduser.assert_called_once_with("~")
        mock_exists.assert_called_once_with(file_test)
        assert len(open_mock.mock_calls) == 0

    @patch("src.app.config_krux_installer.ConfigKruxInstaller.create_app_dir")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.create_app_file")
    @patch("src.app.config_krux_installer.BaseKruxInstaller.get_application_config")
    def test_get_application_config(
        self, mock_get_application_config, mock_create_app_file, mock_create_app_dir
    ):
        mock_create_app_file.return_value = os.path.join("mockfile")
        app = ConfigKruxInstaller()
        app.get_application_config()

        mock_create_app_dir.assert_called_once_with(name="config")
        mock_create_app_file.assert_called_once_with(
            context="config", name="config.ini"
        )
        mock_get_application_config.assert_called_once_with("mockfile")

    def test_build_settings(self):
        settings = MagicMock()
        settings.add_json_panel = MagicMock()
        app = ConfigKruxInstaller()
        app.build_settings(settings)

        utf = ".UTF-8" if sys.platform in ("linux", "darwin") else ""
        json_data = [
            {
                "type": "path",
                "title": "Assets's destination path",
                "desc": "Destination path of downloaded assets",
                "section": "destdir",
                "key": "assets",
            },
            {
                "type": "numeric",
                "title": "Flash baudrate",
                "desc": "Applied baudrate during the flash process",
                "section": "flash",
                "key": "baudrate",
            },
            {
                "type": "options",
                "title": "Locale",
                "desc": "Application locale",
                "section": "locale",
                "key": "lang",
                "options": [
                    f"af_ZA{utf}",
                    f"de_DE{utf}",
                    f"en_US{utf}",
                    f"es_ES{utf}",
                    f"fr_FR{utf}",
                    f"it_IT{utf}",
                    f"ja_JP{utf}",
                    f"ko_KR{utf}",
                    f"nl_NL{utf}",
                    f"pt_BR{utf}",
                    f"ru_RU{utf}",
                    f"zh_CN{utf}",
                ],
            },
        ]

        settings.add_json_panel.assert_has_calls(
            [call("Settings", None, data=json.dumps(json_data))], any_order=True
        )

    @patch("src.app.config_krux_installer.partial")
    def test_skip_on_config_change_linux(self, mock_partial):
        app = ConfigKruxInstaller()
        app.on_config_change(None, "test", key="mock", value="skip")
        assert len(mock_partial.mock_calls) == 0

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.partial")
    def test_on_config_change_linux(self, mock_partial):
        app = ConfigKruxInstaller()
        app.screen_manager = MagicMock()
        app.screen_manager.get_screen = MagicMock()
        app.screens = [
            MagicMock(name="MainScreen"),
            MagicMock(name="FlashScreen"),
            MagicMock(name="WarningWipeScreen"),
            MagicMock(name="WipeScreen"),
            MagicMock(name="WarningBeforeAirgapUpdateScreen"),
            MagicMock(name="AirgapUpdateScreen"),
            MagicMock(name="WarningAfterAirgapUpdateScreen"),
            MagicMock(name="AboutScreen"),
            MagicMock(name="AskPermissionDialoutScreen"),
        ]

        app.on_config_change(None, "locale", key="lang", value="mock")

        # on linux, value stays as-is (no .UTF-8 appended by on_config_change)
        calls_get_screen = [
            call("AskPermissionDialoutScreen"),
            call("MainScreen"),
            call("FlashScreen"),
            call("WarningWipeScreen"),
            call("WipeScreen"),
            call("WarningBeforeAirgapUpdateScreen"),
            call("AirgapUpdateScreen"),
            call("WarningAfterAirgapUpdateScreen"),
            call("AboutScreen"),
        ]

        app.screen_manager.get_screen.assert_has_calls(calls_get_screen, any_order=True)
        mock_partial.assert_called()

    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.partial")
    def test_on_config_change_win32(self, mock_partial):
        app = ConfigKruxInstaller()
        app.screen_manager = MagicMock()
        app.screen_manager.get_screen = MagicMock()
        app.screens = [
            MagicMock(name="MainScreen"),
            MagicMock(name="FlashScreen"),
            MagicMock(name="WarningWipeScreen"),
            MagicMock(name="WipeScreen"),
            MagicMock(name="WarningBeforeAirgapUpdateScreen"),
            MagicMock(name="AirgapUpdateScreen"),
            MagicMock(name="WarningAfterAirgapUpdateScreen"),
            MagicMock(name="AboutScreen"),
        ]

        app.on_config_change(None, "locale", key="lang", value="mock")

        # on win32, value gets .UTF-8 appended
        calls_get_screen = [
            call("MainScreen"),
            call("FlashScreen"),
            call("WarningWipeScreen"),
            call("WipeScreen"),
            call("WarningBeforeAirgapUpdateScreen"),
            call("AirgapUpdateScreen"),
            call("WarningAfterAirgapUpdateScreen"),
            call("AboutScreen"),
        ]

        app.screen_manager.get_screen.assert_has_calls(calls_get_screen, any_order=True)
        mock_partial.assert_called()

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.partial")
    def test_on_config_change_darwin(self, mock_partial):
        app = ConfigKruxInstaller()
        app.screen_manager = MagicMock()
        app.screen_manager.get_screen = MagicMock()
        app.screens = [
            MagicMock(name="MainScreen"),
            MagicMock(name="FlashScreen"),
            MagicMock(name="WarningWipeScreen"),
            MagicMock(name="WipeScreen"),
            MagicMock(name="WarningBeforeAirgapUpdateScreen"),
            MagicMock(name="AirgapUpdateScreen"),
            MagicMock(name="WarningAfterAirgapUpdateScreen"),
            MagicMock(name="AboutScreen"),
        ]

        app.on_config_change(None, "locale", key="lang", value="mock")

        calls_get_screen = [
            call("MainScreen"),
            call("FlashScreen"),
            call("WarningWipeScreen"),
            call("WipeScreen"),
            call("WarningBeforeAirgapUpdateScreen"),
            call("AirgapUpdateScreen"),
            call("WarningAfterAirgapUpdateScreen"),
            call("AboutScreen"),
        ]

        app.screen_manager.get_screen.assert_has_calls(calls_get_screen, any_order=True)
        mock_partial.assert_called()

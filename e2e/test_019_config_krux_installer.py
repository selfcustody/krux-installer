import os
import sys
import json
from unittest.mock import patch, MagicMock, call, mock_open
from kivy.base import EventLoop
from kivy.tests.common import GraphicUnitTest
from src.app.config_krux_installer import ConfigKruxInstaller


class TestConfigKruxInstaller(GraphicUnitTest):

    @classmethod
    def teardown_class(cls):
        EventLoop.exit()

    @patch("src.app.config_krux_installer.kv_resources.resource_add_path")
    @patch("src.app.config_krux_installer.LabelBase.register")
    @patch("src.app.config_krux_installer.os.path.abspath", side_effect=["mock/path/assets", "mock//path/i18n"])
    def test_init(self, mock_abspath, mock_register, mock_resource_add_path):
        with patch.dict(sys.__dict__, { "frozen": False }): 
            # Initialize ConfigKruxInstaller instance
            ConfigKruxInstaller()
        
            # Check if resource_add_path is called with the mocked _MEIPASS
            mock_register.assert_called_once_with(
                "Roboto",
                "mock/path/assets/NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
            )

    @patch("src.app.config_krux_installer.kv_resources.resource_add_path")
    @patch("src.app.config_krux_installer.LabelBase.register")
    def test_init_frozen_branch(self, mock_register, mock_resource_add_path):
        with patch.dict(sys.__dict__, { "_MEIPASS": "/mocked/path", "frozen": True }): 
            # Initialize ConfigKruxInstaller instance
            installer = ConfigKruxInstaller()
        
            # Check if resource_add_path is called with the mocked _MEIPASS
            mock_resource_add_path.assert_called_with("/mocked/path")
            mock_register.assert_called_once_with(
                "Roboto",
                "/mocked/path/assets/NotoSansCJK_CY_JP_SC_KR_VI_Krux.ttf"
            )
        
            # Check if the assets_path and i18n_path are set based on _MEIPASS
            self.assertEqual(installer.assets_path, "/mocked/path/assets")
            self.assertEqual(installer.i18n_path, "/mocked/path/src/i18n")

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
            "Couldn't possible to setup locale: OS 'mockos' not implemented"
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

        # patch assertions
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

        # patch assertions
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

        # patch assertions
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

        # patch assertions
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

        # patch assertions
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

        # patch assertions
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

        # patch assertions
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

        # patch assertions
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

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True, True])
    @patch("builtins.open", new_callable=mock_open)
    def test_skip_create_app_file_linux(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join("mockdir", ".config", "krux-installer", "config.ini")

        self.assertEqual(file, file_test)

        # patch assertions
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

        # patch assertions
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

        # patch assertions
        mock_exists.assert_called_once_with(file_test)
        assert len(open_mock.mock_calls) == 0

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[False, False])
    @patch("builtins.open", new_callable=mock_open)
    def test_create_app_file_darwin(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join(
            "mockdir",
            ".config",
            "krux-installer",
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

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.os.path.expanduser", return_value="mockdir")
    @patch("src.app.config_krux_installer.os.path.exists", side_effect=[True, True])
    @patch("builtins.open", new_callable=mock_open)
    def test_skip_create_app_file_darwin(self, open_mock, mock_exists, mock_expanduser):
        app = ConfigKruxInstaller()
        file = app.create_app_file(context="config", name="config.ini")
        file_test = os.path.join(
            "mockdir",
            ".config",
            "krux-installer",
            "config.ini",
        )

        self.assertEqual(file, file_test)

        # patch assertions
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

        # patch assertions
        mock_create_app_dir.assert_called_once_with(name="config")
        mock_create_app_file.assert_called_once_with(
            context="config", name="config.ini"
        )
        mock_get_application_config.assert_called_once_with("mockfile")

    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.create_app_dir", return_value="mockdir")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.get_system_lang", return_value="en_US.UTF-8")
    @patch("src.app.config_krux_installer.os.path.isfile", return_value=True)
    def test_build_config_posix_no_default_lang(
        self,
        mock_isfile,
        mock_get_system_lang,
        mock_create_app_dir
    ):
        config = MagicMock()
        config.setdefaults = MagicMock()

        app = ConfigKruxInstaller()
        app.i18n_path = "mock/i18n"
        app.build_config(config)

        # patch assertions
        mock_create_app_dir.assert_called_once_with(name="local")
        mock_isfile.assert_called_once_with("mock/i18n/en_US.UTF-8.json")
        config.setdefaults.assert_has_calls(
            [
                call("destdir", {"assets": "mockdir"}),
                call("flash", {"baudrate": 1500000}),
                call("locale", {"lang": "en_US.UTF-8"}),
            ]
        )
    
    @patch("sys.platform", "linux")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.create_app_dir", return_value="mockdir")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.get_system_lang", return_value="mo_CK.UTF-8")
    @patch("src.app.config_krux_installer.os.path.isfile", return_value=False)
    def test_build_config_posix_default_lang(
        self,
        mock_isfile,
        mock_get_system_lang,
        mock_create_app_dir
    ):
        config = MagicMock()
        config.setdefaults = MagicMock()

        app = ConfigKruxInstaller()
        app.i18n_path = "mock/i18n"
        app.build_config(config)

        # patch assertions
        mock_create_app_dir.assert_called_once_with(name="local")
        mock_isfile.assert_called_once_with("mock/i18n/mo_CK.UTF-8.json")
        config.setdefaults.assert_has_calls(
            [
                call("destdir", {"assets": "mockdir"}),
                call("flash", {"baudrate": 1500000}),
                call("locale", {"lang": "en_US.UTF-8"}),
            ]
        )

    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.create_app_dir", return_value="mockdir")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.get_system_lang", return_value="en_US")
    @patch("src.app.config_krux_installer.os.path.isfile", return_value=True)
    def test_build_config_windows_default_lang(
        self,
        mock_isfile,
        mock_get_system_lang,
        mock_create_app_dir
    ):
        config = MagicMock()
        config.setdefaults = MagicMock()

        app = ConfigKruxInstaller()
        app.i18n_path = "mock/i18n"
        app.build_config(config)
        
        # patch assertions
        mock_create_app_dir.assert_called_once_with(name="local")
        mock_get_system_lang.assert_called_once()
        mock_isfile.assert_called_once_with("mock/i18n/en_US.UTF-8.json")
        config.setdefaults.assert_has_calls(
            [
                call("destdir", {"assets": "mockdir"}),
                call("flash", {"baudrate": 1500000}),
                call("locale", {"lang": "en_US"}),
            ]
        )
    
    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.create_app_dir", return_value="mockdir")
    @patch("src.app.config_krux_installer.ConfigKruxInstaller.get_system_lang", return_value="mo_CK")
    @patch("src.app.config_krux_installer.os.path.isfile", return_value=False)
    def test_build_config_windows_no_default_lang(
        self,
        mock_isfile,
        mock_get_system_lang,
        mock_create_app_dir
    ):
        config = MagicMock()
        config.setdefaults = MagicMock()

        app = ConfigKruxInstaller()
        app.i18n_path = "mock/i18n"
        app.build_config(config)
        
        # patch assertions
        mock_create_app_dir.assert_called_once_with(name="local")
        mock_get_system_lang.assert_called_once()
        mock_isfile.assert_called_once_with("mock/i18n/mo_CK.UTF-8.json")
        config.setdefaults.assert_has_calls(
            [
                call("destdir", {"assets": "mockdir"}),
                call("flash", {"baudrate": 1500000}),
                call("locale", {"lang": "en_US"}),
            ]
        )

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

        # patch assertions
        settings.add_json_panel.assert_has_calls(
            [call("Settings", None, data=json.dumps(json_data))], any_order=True
        )

    @patch("src.app.config_krux_installer.partial")
    def test_skip_on_config_change_linux(self, mock_partial):
        app = ConfigKruxInstaller()

        # Do tests
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
            MagicMock(name="SelectVersionScreen"),
            MagicMock(name="SelectOldVersionScreen"),
            MagicMock(name="WarningAlreadyDownloadedScreen"),
            MagicMock(name="WarningBetaScreen"),
            MagicMock(name="VerifyStableZipScreen"),
            MagicMock(name="UnzipStableScreen"),
            MagicMock(name="AskPermissionDialoutScreen"),
        ]

        # Do tests
        app.on_config_change(None, "locale", key="lang", value="mock")

        # patch assertions
        calls_get_screen = [
            call("MainScreen"),
            call("SelectVersionScreen"),
            call("SelectOldVersionScreen"),
            call("WarningAlreadyDownloadedScreen"),
            call("WarningBetaScreen"),
            call("VerifyStableZipScreen"),
            call("UnzipStableScreen"),
            call("AskPermissionDialoutScreen"),
        ]

        calls_partial = [
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="version",
                value=app.screen_manager.get_screen().version,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="device",
                value=app.screen_manager.get_screen().device,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="flash",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="wipe",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="settings",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="about",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
        ]

        app.screen_manager.get_screen.assert_has_calls(calls_get_screen, any_order=True)
        mock_partial.assert_has_calls(calls_partial)

    @patch("sys.platform", "win32")
    @patch("src.app.config_krux_installer.partial")
    def test_on_config_change_win32(self, mock_partial):

        app = ConfigKruxInstaller()

        app.screen_manager = MagicMock()
        app.screen_manager.get_screen = MagicMock()
        app.screens = [
            MagicMock(name="MainScreen"),
            MagicMock(name="SelectVersionScreen"),
            MagicMock(name="SelectOldVersionScreen"),
            MagicMock(name="WarningAlreadyDownloadedScreen"),
            MagicMock(name="WarningBetaScreen"),
            MagicMock(name="VerifyStableZipScreen"),
            MagicMock(name="UnzipStableScreen"),
        ]

        # Do tests
        app.on_config_change(None, "locale", key="lang", value="mock")

        # patch assertions
        calls_get_screen = [
            call("MainScreen"),
            call("SelectVersionScreen"),
            call("SelectOldVersionScreen"),
            call("WarningAlreadyDownloadedScreen"),
            call("WarningBetaScreen"),
            call("VerifyStableZipScreen"),
            call("UnzipStableScreen"),
        ]

        calls_partial = [
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="version",
                value=app.screen_manager.get_screen().version,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="device",
                value=app.screen_manager.get_screen().device,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="flash",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="wipe",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="settings",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="about",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock.UTF-8",
            ),
        ]

        app.screen_manager.get_screen.assert_has_calls(calls_get_screen, any_order=True)
        mock_partial.assert_has_calls(calls_partial)

    @patch("sys.platform", "darwin")
    @patch("src.app.config_krux_installer.partial")
    def test_on_config_change_darwin(self, mock_partial):

        app = ConfigKruxInstaller()

        app.screen_manager = MagicMock()
        app.screen_manager.get_screen = MagicMock()
        app.screens = [
            MagicMock(name="MainScreen"),
            MagicMock(name="SelectVersionScreen"),
            MagicMock(name="SelectOldVersionScreen"),
            MagicMock(name="WarningAlreadyDownloadedScreen"),
            MagicMock(name="WarningBetaScreen"),
            MagicMock(name="VerifyStableZipScreen"),
            MagicMock(name="UnzipStableScreen"),
        ]

        # Do tests
        app.on_config_change(None, "locale", key="lang", value="mock")

        # patch assertions
        calls_get_screen = [
            call("MainScreen"),
            call("SelectVersionScreen"),
            call("SelectOldVersionScreen"),
            call("WarningAlreadyDownloadedScreen"),
            call("WarningBetaScreen"),
            call("VerifyStableZipScreen"),
            call("UnzipStableScreen"),
        ]

        calls_partial = [
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="version",
                value=app.screen_manager.get_screen().version,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="device",
                value=app.screen_manager.get_screen().device,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="flash",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="wipe",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="settings",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="about",
                value=None,
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
            call(
                app.screen_manager.get_screen().update,
                name="ConfigKruxInstaller",
                key="locale",
                value="mock",
            ),
        ]

        app.screen_manager.get_screen.assert_has_calls(calls_get_screen, any_order=True)
        mock_partial.assert_has_calls(calls_partial)

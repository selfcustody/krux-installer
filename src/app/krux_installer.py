# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
krux_installer.py
"""

import tempfile
from kivy.lang.builder import Builder
from kivy.core.window import Window
from .base_krux_installer import BaseKruxInstaller, KIVY_FILE


class KruxInstallerApp(BaseKruxInstaller):
    """KruxInstallerApp is the Root widget"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._initialize_window()
        self._initialize_kv_file()

    def _initialize_window(self):
        Window.size = (640, 800)
        self.debug(f"Window: {Window.size}")

    def _initialize_kv_file(self):
        Builder.load_file(KIVY_FILE)

    def build_config(self, config):
        """Create default configurations for app"""
        destdir = tempfile.mkdtemp()

        config.setdefaults("destdir", {"assets": destdir})

        config.setdefaults(
            "flash",
            {
                "baudrate": 1500000,
            },
        )

        config.setdefaults(
            "locale",
            {
                "lang": "en-US",
            },
        )

    def build_settings(self, settings):
        """Create settings panel"""
        jsondata = """[
            { 
                "type": "path",
                "title": "Assets's destination path",
                "desc": "Destination path of downloaded assets",
                "section": "destdir",
                "key": "assets"
            },            
            { 
                "type": "numeric",
                "title": "Flash baudrate",
                "desc": "Applied baudrate during the flash process",
                "section": "krux-installer-config",
                "key": "baudrate"
            },            
            { 
                "type": "options",
                "title": "Locale",
                "desc": "Application locale",
                "section": "krux-installer-config",
                "key": "locale",
                "options": ["en-US", "pt-BR"]
            }
        ]"""
        settings.add_json_panel("Settings", self.config, data=jsondata)

    def build(self):
        """Create the Root widget with an ScreenManager as manager for its sub-widgets"""
        for screen in self.screens:
            msg = f"adding screen '{screen.name}'"
            self.debug(msg)
            self.screen_manager.add_widget(screen)

        return self.screen_manager

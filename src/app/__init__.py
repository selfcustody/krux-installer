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
__init__.py
"""

import os
import sys
from functools import partial
from kivy.clock import Clock

# fix: red circles appearing when other inputs are received instead of the left mouse button.

os.environ.setdefault("KIVY_MOUSE_MODE", "disable_multitouch")

# pylint: disable=wrong-import-position
from kivy.config import Config

Config.set("input", "mouse", "mouse,disable_multitouch")

from kivy.core.window import Window
from src.app.config_krux_installer import ConfigKruxInstaller
from src.app.screens.about_screen import AboutScreen
from src.app.screens.ask_permission_dialout_screen import AskPermissionDialoutScreen
from src.app.screens.download_beta_screen import DownloadBetaScreen
from src.app.screens.download_selfcustody_pem_screen import DownloadSelfcustodyPemScreen
from src.app.screens.download_stable_zip_screen import DownloadStableZipScreen
from src.app.screens.download_stable_zip_sha256_screen import (
    DownloadStableZipSha256Screen,
)
from src.app.screens.download_stable_zip_sig_screen import DownloadStableZipSigScreen
from src.app.screens.error_screen import ErrorScreen
from src.app.screens.flash_screen import FlashScreen
from src.app.screens.greetings_screen import GreetingsScreen
from src.app.screens.main_screen import MainScreen
from src.app.screens.select_device_screen import SelectDeviceScreen
from src.app.screens.select_old_version_screen import SelectOldVersionScreen
from src.app.screens.select_version_screen import SelectVersionScreen
from src.app.screens.unzip_stable_screen import UnzipStableScreen
from src.app.screens.verify_stable_zip_screen import VerifyStableZipScreen
from src.app.screens.warning_already_downloaded_screen import (
    WarningAlreadyDownloadedScreen,
)
from src.app.screens.warning_beta_screen import WarningBetaScreen
from src.app.screens.warning_wipe_screen import WarningWipeScreen
from src.app.screens.wipe_screen import WipeScreen
from src.app.screens.airgap_update_screen import AirgapUpdateScreen
from src.app.screens.warning_before_airgap_update_screen import (
    WarningBeforeAirgapUpdateScreen,
)
from src.app.screens.warning_after_airgap_update_screen import (
    WarningAfterAirgapUpdateScreen,
)

# pylint: enable=wrong-import-position

# Default screen parent map — used to initialize the instance attribute.
# Maps each screen to its parent in the UI tree.
# ESC navigates to the parent; None means ESC exits the app.
# FlashScreen's parent is dynamic and set at runtime by the screen that navigates to it.
SCREEN_PARENTS = {
    "GreetingsScreen": None,
    "MainScreen": "GreetingsScreen",
    "SelectVersionScreen": "MainScreen",
    "SelectOldVersionScreen": "SelectVersionScreen",
    "WarningBetaScreen": "SelectVersionScreen",
    "SelectDeviceScreen": "MainScreen",
    "AboutScreen": "MainScreen",
    "WarningAlreadyDownloadedScreen": "MainScreen",
    "DownloadStableZipScreen": "MainScreen",
    "DownloadStableZipSha256Screen": "DownloadStableZipScreen",
    "DownloadStableZipSigScreen": "DownloadStableZipSha256Screen",
    "DownloadSelfcustodyPemScreen": "DownloadStableZipSigScreen",
    "VerifyStableZipScreen": "DownloadSelfcustodyPemScreen",
    "UnzipStableScreen": "VerifyStableZipScreen",
    "DownloadBetaScreen": "MainScreen",
    "WarningWipeScreen": "MainScreen",
    "WipeScreen": "WarningWipeScreen",
    "WarningBeforeAirgapUpdateScreen": "MainScreen",
    "AirgapUpdateScreen": "WarningBeforeAirgapUpdateScreen",
    "WarningAfterAirgapUpdateScreen": "MainScreen",
    "FlashScreen": None,  # set dynamically at runtime
    "ErrorScreen": "GreetingsScreen",
}


class KruxInstallerApp(ConfigKruxInstaller):
    """KruxInstallerApp is the Root widget"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (1000, 800)
        self.debug(f"Window.size={Window.size}")
        Window.clearcolor = (0.9, 0.9, 0.9, 1)
        self.screen_parents = dict(SCREEN_PARENTS)

    def build(self):
        """Create the Root widget with an ScreenManager as manager for its sub-widgets"""
        screens = []
        screens.append(GreetingsScreen())

        if sys.platform == "linux":
            screens.append(AskPermissionDialoutScreen())

        screens = screens + [
            MainScreen(),
            SelectDeviceScreen(),
            SelectVersionScreen(),
            SelectOldVersionScreen(),
            WarningBetaScreen(),
            AboutScreen(),
            DownloadStableZipScreen(),
            DownloadStableZipSha256Screen(),
            DownloadStableZipSigScreen(),
            DownloadSelfcustodyPemScreen(),
            VerifyStableZipScreen(),
            UnzipStableScreen(),
            DownloadBetaScreen(),
            WarningAlreadyDownloadedScreen(),
            WarningWipeScreen(),
            FlashScreen(),
            WarningBeforeAirgapUpdateScreen(),
            WarningAfterAirgapUpdateScreen(),
            AirgapUpdateScreen(),
            WipeScreen(),
            ErrorScreen(),
        ]

        for screen in screens:
            msg = f"adding screen '{screen.name}'"
            self.debug(msg)
            self.screen_manager.add_widget(screen)

        Window.bind(on_key_down=self._on_key_down)

        return self.screen_manager

    def _reset_main_screen(self):
        """Reset MainScreen device to default when navigating back to GreetingsScreen"""
        main_screen = self.screen_manager.get_screen("MainScreen")
        fn = partial(
            main_screen.update,
            name="KruxInstallerApp",
            key="device",
            value="select a new one",
        )
        Clock.schedule_once(fn, 0)

    def _on_key_down(self, _window, key, *_):
        # key == 27 is ESC
        if key == 27:
            current = self.screen_manager.current
            parent = self.screen_parents.get(current)

            if parent is None:
                self.stop()
                return True

            if parent == "GreetingsScreen":
                self._reset_main_screen()

            self.screen_manager.transition.direction = "right"
            self.screen_manager.current = parent
            return True

        return False

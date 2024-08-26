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
wipe_screen.py
"""
import sys
import threading
import traceback
from functools import partial
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from src.utils.flasher.wiper import Wiper
from src.app.screens.base_flash_screen import BaseFlashScreen


class WipeScreen(BaseFlashScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="wipe_screen", name="WipeScreen", **kwargs)
        self.wiper = None
        self.success = False
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def on_pre_enter(self):
        self.ids[f"{self.id}_grid"].clear_widgets()

        def on_print_callback(*args, **kwargs):
            text = " ".join(str(x) for x in args)
            self.info(text)

            text = text.replace(
                "\x1b[32m\x1b[1m[INFO]\x1b[0m", "[color=#00ff00]INFO[/color]"
            )
            text = text.replace(
                "\x1b[33mISP loaded", "[color=#efcc00]ISP loaded[/color]"
            )
            text = text.replace(
                "\x1b[33mInitialize K210 SPI Flash",
                "[color=#efcc00]Initialize K210 SPI Flash[/color]",
            )
            text = text.replace("Flash ID: \x1b[33m", "Flash ID: [color=#efcc00]")
            text = text.replace(
                "\x1b[0m, unique ID: \x1b[33m", "[/color], unique ID: [color=#efcc00]"
            )
            text = text.replace("\x1b[0m, size: \x1b[33m", "[/color], size: ")
            text = text.replace("\x1b[0m MB", "[/color] MB")
            text = text.replace("\x1b[0m", "")
            text = text.replace("\x1b[33m", "")
            text = text.replace(
                "[INFO] Erasing the whole SPI Flash",
                "[color=#00ff00]INFO[/color][color=#efcc00] Erasing the whole SPI Flash [/color]",
            )

            text = text.replace(
                "\x1b[31m\x1b[1m[ERROR]\x1b[0m", "[color=#ff0000]ERROR[/color]"
            )

            self.output.append(text)

            if len(self.output) > 18:
                del self.output[:1]

            if "SPI Flash erased." in text:
                self.trigger()

            self.ids[f"{self.id}_info"].text = "\n".join(self.output)

        def on_ref_press(*args):
            if args[1] == "Back":
                self.set_screen(name="MainScreen", direction="right")

            elif args[1] == "Quit":
                App.get_running_app().stop()

            else:
                self.redirect_error(f"Invalid ref: {args[1]}")

        def on_trigger_callback(dt):
            self.success = True
            del self.output[4:]
            self.ids[f"{self.id}_loader"].source = self.done_img
            self.ids[f"{self.id}_loader"].reload()
            done = self.translate("DONE")
            back = self.translate("Back")
            quit = self.translate("Quit")
            if sys.platform in ("linux", "win32"):
                size = self.SIZE_M
            else:
                size = self.SIZE_M

            self.ids[f"{self.id}_progress"].text = "".join(
                [
                    f"[size={size}sp][b]{done}![/b][/size]",
                    "\n",
                    f"[size={size}sp]",
                    "[color=#00FF00]",
                    f"[ref=Back][u]{back}[/u][/ref]",
                    "[/color]",
                    "        ",
                    "[color=#EFCC00]",
                    f"[ref=Quit][u]{quit}[/u][/ref]",
                    "[/color]",
                ]
            )
            self.ids[f"{self.id}_progress"].bind(on_ref_press=on_ref_press)

        setattr(WipeScreen, "on_print_callback", on_print_callback)
        setattr(WipeScreen, "on_trigger_callback", on_trigger_callback)

        self.make_subgrid(
            wid=f"{self.id}_subgrid", rows=3, root_widget=f"{self.id}_grid"
        )

        self.make_image(
            wid=f"{self.id}_loader",
            source=self.load_img,
            root_widget=f"{self.id}_subgrid",
        )

        self.make_label(
            wid=f"{self.id}_progress",
            text="",
            root_widget=f"{self.id}_subgrid",
            markup=True,
            halign="center",
        )

        self.make_label(
            wid=f"{self.id}_info",
            text="",
            root_widget=f"{self.id}_grid",
            markup=True,
            halign="justify",
        )

    def on_enter(self):
        """
        Event fired when the screen is displayed and the entering animation is complete.
        """
        self.debug("Staring wipe...")
        if self.wiper is not None:
            please = self.translate("PLEASE DO NOT UNPLUG YOUR DEVICE")
            if sys.platform in ("linux", "win32"):
                sizes = [self.SIZE_M, self.SIZE_PP]
            else:
                sizes = [self.SIZE_MM, self.SIZE_MP]

            self.ids[f"{self.id}_progress"].text = f"[size={sizes[0]}sp][b]{please}[/b]"
            self.output = []
            self.progress = ""
            self.is_done = False
            self.trigger = getattr(self.__class__, "on_trigger_callback")
            self.wiper.ktool.__class__.print_callback = getattr(
                self.__class__, "on_print_callback"
            )
            on_process_callback = partial(self.wiper.wipe, device=self.device)
            self.thread = threading.Thread(name=self.name, target=on_process_callback)

            # if anything wrong happen, show it
            def hook(err):
                msg = "".join(
                    traceback.format_exception(
                        err.exc_type, err.exc_value, err.exc_traceback
                    )
                )
                self.error(msg)
                done = self.translate("DONE")
                back = self.translate("Back")
                quit = self.translate("Quit")

                self.ids[f"{self.id}_progress"].text = "".join(
                    [
                        f"[size={sizes[0]}]",
                        f"[color=#FF0000]{"Wipe failed" if not self.success else done}[/color]",
                        "[/size]",
                        "\n",
                        "\n",
                        f"[size={sizes[0]}]" "[color=#00FF00]",
                        f"[ref=Back][u]{back}[/u][/ref]",
                        "[/color]",
                        "        ",
                        "[color=#EFCC00]",
                        f"[ref=Quit][u]{quit}[/u][/ref]",
                        "[/color]",
                        "[/size]",
                    ]
                )

                self.ids[f"{self.id}_info"].text = "".join(
                    [
                        f"[size={sizes[1]}]",
                        msg,
                        "[/size]",
                    ]
                )

            # hook what happened
            threading.excepthook = hook
            self.thread.start()
        else:
            self.redirect_error("Wiper isnt configured")

    def update(self, *args, **kwargs):
        """Update screen with firmware key. Should be called before `on_enter`"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "MainScreen",
            "WarningWipeScreen",
            "WipeScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            self.redirect_error(f"Invalid screen name: {name}")
            return

        key = kwargs.get("key")
        value = kwargs.get("value")

        if key == "locale":
            if value is not None:
                self.locale = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': {value}")

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        elif key == "device":
            if value is not None:
                self.device = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': {value}")

        elif key == "wiper":
            if value is not None:
                self.wiper = Wiper()
                self.wiper.baudrate = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': {value}")

        else:
            raise ValueError(f'Invalid key: "{key}"')

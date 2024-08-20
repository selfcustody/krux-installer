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
main_screen.py
"""
import sys
import threading
import traceback
from functools import partial
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.vertex_instructions import Rectangle
from kivy.graphics.context_instructions import Color
from src.app.screens.base_flash_screen import BaseFlashScreen
from src.utils.flasher import Flasher


class FlashScreen(BaseFlashScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="flash_screen", name="FlashScreen", **kwargs)
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
            text = text.replace("\rProgramming", "Programming")

            if "INFO" in text:
                self.output.append(text)
                if "Rebooting" in text:
                    self.trigger()

            elif "Programming BIN" in text:
                self.output[-1] = text

            elif "*" in text:
                self.output.append("*")
                self.output.append("")

            if len(self.output) > 18:
                del self.output[:1]

            self.ids[f"{self.id}_info"].text = "\n".join(self.output)

        def on_process_callback(
            file_type: str, iteration: int, total: int, suffix: str
        ):
            percent = (iteration / total) * 100
            flashing = self.translate("Flashing")
            at = self.translate("at")

            self.ids[f"{self.id}_progress"].text = "".join(
                [
                    f"[font={FlashScreen.get_font_name()}]",
                    f"[size=100sp]{percent:.2f} %[/size]",
                    "\n",
                    "[size=28sp]",
                    f"{flashing} ",
                    "[color=#efcc00]",
                    "[b]",
                    file_type,
                    "[/b]",
                    "[/color]",
                    f" {at} ",
                    "[color=#efcc00]",
                    "[b]",
                    suffix,
                    "[/b]",
                    "[/color]",
                    "[/size]",
                    "[/font]",
                ]
            )

        def on_ref_press(*args):
            if args[1] == "Back":
                self.set_screen(name="MainScreen", direction="right")

            elif args[1] == "Quit":
                App.get_running_app().stop()

            else:
                self.redirect_error(f"Invalid ref: {args[1]}")

        def on_trigger_callback(dt):
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

            self.ids[f"{self.id}_progress"].text = "\n".join(
                [
                    "".join(
                        [
                            f"[font={FlashScreen.get_font_name()}]",
                            f"[size={size}sp][b]{done}![/b][/size]",
                            "[/font]",
                        ]
                    ),
                    "",
                    "",
                    "".join(
                        [
                            f"[font={FlashScreen.get_font_name()}]",
                            f"[size={size}sp]",
                            f"[color=#00FF00][ref=Back]{back}[/ref][/color]",
                            "        ",
                            f"[color=#EFCC00][ref=Quit]{quit}[/ref][/color]",
                            "[/font]",
                        ]
                    ),
                ]
            )
            self.ids[f"{self.id}_progress"].bind(on_ref_press=on_ref_press)

        setattr(FlashScreen, "on_print_callback", on_print_callback)
        setattr(FlashScreen, "on_process_callback", on_process_callback)
        setattr(FlashScreen, "on_trigger_callback", on_trigger_callback)

        self.make_subgrid(
            wid=f"{self.id}_subgrid", rows=2, root_widget=f"{self.id}_grid"
        )

        self.make_image(
            wid=f"{self.id}_loader",
            source=self.warn_img,
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
        if hasattr(self, "flasher"):
            self.output = []
            self.trigger = getattr(self.__class__, "on_trigger_callback")
            self.flasher.ktool.__class__.print_callback = getattr(
                self.__class__, "on_print_callback"
            )
            on_process_callback = partial(
                self.flasher.flash,
                callback=getattr(self.__class__, "on_process_callback"),
            )
            self.thread = threading.Thread(name=self.name, target=on_process_callback)

            if sys.platform in ("linux", "win32"):
                sizes = [self.SIZE_M, self.SIZE_P]
            else:
                sizes = [self.SIZE_MM, self.SIZE_MP]

            # if anything wrong happen, show it
            def hook(err):
                msg = "".join(
                    traceback.format_exception(
                        err.exc_type, err.exc_value, err.exc_traceback
                    )
                )
                self.error(msg)

                back = self.translate("Back")
                quit = self.translate("Quit")
                self.ids[f"{self.id}_progress"].text = "".join(
                    [
                        "[font=terminus]",
                        f"[size={sizes[0]}]",
                        "[color=#FF0000]Flash failed[/color]",
                        "[/size]",
                        "[/font]," "\n",
                        "\n",
                        f"[size={sizes[0]}]",
                        f"[font={FlashScreen.get_font_name()}]"
                        f"[color=#00FF00][ref=Back]{back}[/ref][/color]",
                        "        ",
                        f"[color=#EFCC00][ref=Quit]{quit}[/ref][/color]",
                        "[/size]",
                        "[/font]",
                    ]
                )

                self.ids[f"{self.id}_info"].text = "".join(
                    [
                        "[font=terminus]",
                        f"[size={sizes[1]}]",
                        msg,
                        "[/size]",
                        "[/font]",
                    ]
                )

            # hook what happened
            threading.excepthook = hook

            # start thread
            self.thread.start()
        else:
            self.redirect_error("Flasher isnt configured")

    def update(self, *args, **kwargs):
        """Update screen with firmware key. Should be called before `on_enter`"""
        name = kwargs.get("name")
        key = kwargs.get("key")
        value = kwargs.get("value")

        if name in (
            "ConfigKruxInstaller",
            "UnzipStableScreen",
            "DownloadBetaScreen",
            "FlashScreen",
        ):
            self.debug(f"Updating {self.name} from {name}...")
        else:
            raise ValueError(f"Invalid screen name: {name}")

        key = kwargs.get("key")
        value = kwargs.get("value")

        if key == "locale":
            if value is not None:
                self.locale = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "canvas":
            # prepare background
            with self.canvas.before:
                Color(0, 0, 0, 1)
                Rectangle(size=(Window.width, Window.height))

        elif key == "baudrate":
            if value is not None:
                self.baudrate = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "firmware":
            if value is not None:
                self.firmware = value
            else:
                self.redirect_error(f"Invalid value for key '{key}': '{value}'")

        elif key == "flasher":
            self.flasher = Flasher()
            self.flasher.firmware = self.firmware
            self.flasher.baudrate = self.baudrate

        elif key == "exception":
            self.redirect_error("")
        else:
            self.redirect_error(f'Invalid key: "{key}"')

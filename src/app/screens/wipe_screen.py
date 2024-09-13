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
from src.utils.flasher.wiper import Wiper
from src.app.screens.base_flash_screen import BaseFlashScreen


class WipeScreen(BaseFlashScreen):
    """Flash screen is where flash occurs"""

    def __init__(self, **kwargs):
        super().__init__(wid="wipe_screen", name="WipeScreen", **kwargs)
        self.wiper = None
        self.success = False
        self.progress = ""
        self.device = None
        fn = partial(self.update, name=self.name, key="canvas")
        Clock.schedule_once(fn, 0)

    def build_on_data(self):
        """
        Build a streaming IO static method using
        some instance variables for flash procedure
        when KTool.print_callback is called

        (useful for to be used in tests)
        """

        # pylint: disable=unused-argument
        def on_data(*args, **kwargs):
            text = " ".join(str(x) for x in args)
            self.info(text)
            text = WipeScreen.parse_general_output(text)
            text = text.replace(
                "[INFO] Erasing the whole SPI Flash",
                "".join(
                    [
                        "[color=#00ff00]INFO[/color]",
                        "[color=#efcc00] Erasing the whole SPI Flash [/color]",
                    ]
                ),
            )
            text = text.replace(
                "\x1b[31m\x1b[1m[ERROR]\x1b[0m", "[color=#ff0000]ERROR[/color]"
            )
            self.output.append(text)

            if len(self.output) > 18:
                del self.output[:1]

            if "SPI Flash erased." in text:
                self.is_done = True
                # pylint: disable=not-callable
                self.done()

            self.ids[f"{self.id}_info"].text = "\n".join(self.output)

        setattr(WipeScreen, "on_data", on_data)

    # pylint: disable=unused-argument
    def on_pre_enter(self, *args):
        self.ids[f"{self.id}_grid"].clear_widgets()
        self.build_on_data()
        self.build_on_done()

        def on_ref_press(*args):
            if args[1] == "Back":
                self.set_screen(name="MainScreen", direction="right")

            elif args[1] == "Quit":
                App.get_running_app().stop()

            else:
                msg = f"Invalid ref: {args[1]}"
                exc = RuntimeError(msg)
                self.error(msg)
                self.redirect_exception(exception=exc)

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
            halign="center",
        )
        self.ids[f"{self.id}_progress"].bind(on_ref_press=on_ref_press)

        self.make_label(
            wid=f"{self.id}_info",
            text="",
            root_widget=f"{self.id}_grid",
            halign="justify",
        )

    # pylint: disable=unused-argument
    def on_enter(self, *args):
        """
        Event fired when the screen is displayed and the entering animation is complete.
        """
        self.done = getattr(WipeScreen, "on_done")
        self.wiper.ktool.__class__.print_callback = getattr(WipeScreen, "on_data")
        on_process = partial(self.wiper.wipe, device=self.device)
        self.thread = threading.Thread(name=self.name, target=on_process)

        please = self.translate("PLEASE DO NOT UNPLUG YOUR DEVICE")
        if sys.platform in ("linux", "win32"):
            sizes = [self.SIZE_M, self.SIZE_PP]
        else:
            sizes = [self.SIZE_MM, self.SIZE_MP]

        self.ids[f"{self.id}_progress"].text = f"[size={sizes[0]}sp][b]{please}[/b]"

        # if anything wrong happen, show it
        def hook(err):
            if not self.is_done:
                trace = traceback.format_exception(
                    err.exc_type, err.exc_value, err.exc_traceback
                )
                msg = "".join(trace)
                self.error(msg)

                done = self.translate("DONE")
                back = self.translate("Back")
                _quit = self.translate("Quit")

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
                        f"[ref=Quit][u]{_quit}[/u][/ref]",
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

    def update(self, *args, **kwargs):
        """Update screen with firmware key. Should be called before `on_enter`"""
        name = str(kwargs.get("name"))
        key = str(kwargs.get("key"))
        value = kwargs.get("value")

        def on_update():
            if key == "device":
                setattr(self, "device", value)

            if key == "wiper":
                setattr(self, "wiper", Wiper())
                setattr(getattr(self, "wiper"), "baudrate", value)

        setattr(WipeScreen, "on_update", on_update)
        self.update_screen(
            name=name,
            key=key,
            value=value,
            allowed_screens=(
                "ConfigKruxInstaller",
                "MainScreen",
                "WarningWipeScreen",
                "WipeScreen",
            ),
            on_update=getattr(WipeScreen, "on_update"),
        )

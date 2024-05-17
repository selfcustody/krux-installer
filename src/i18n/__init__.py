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
from easy_i18n.t import Ai18n

a_i18n = Ai18n(locales=["en_US.UTF-8", "pt_BR.UTF-8", "es_ES.UTF-8", "ru_RU.UTF-8"])

T = a_i18n.translate

# Version
a_i18n.add(k="Version", message="Version", module="main_screen", locale="en_US.UTF-8")
a_i18n.add(k="Version", message="Versão", module="main_screen", locale="pt_BR.UTF-8")
a_i18n.add(k="Version", message="Versión", module="main_screen", locale="es_ES.UTF-8")
a_i18n.add(k="Version", message="Версия", module="main_screen", locale="ru_RU.UTF-8")

# Device
a_i18n.add(k="Device", message="Device", module="main_screen", locale="en_US.UTF-8")
a_i18n.add(
    k="Device", message="Dispositivo", module="main_screen", locale="pt_BR.UTF-8"
)
a_i18n.add(
    k="Device", message="Dispositivo", module="main_screen", locale="es_ES.UTF-8"
)
a_i18n.add(k="Device", message="Устройство", module="main_screen", locale="ru_RU.UTF-8")

# select a new one
a_i18n.add(
    k="select a new one",
    message="select a new one",
    module="main_screen",
    locale="en_US.UTF-8",
)
a_i18n.add(
    k="select a new one",
    message="selecione um novo",
    module="main_screen",
    locale="pt_BR.UTF-8",
)
a_i18n.add(
    k="select a new one",
    message="seleccione uno nuevo",
    module="main_screen",
    locale="_s-.UTF-8",
)
a_i18n.add(
    k="select a new one",
    message="выберите новый",
    module="main_screen",
    locale="ru_RU.UTF-8",
)

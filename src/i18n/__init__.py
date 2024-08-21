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
import re
import os
import json
from easy_i18n.t import Ai18n
from src.utils.trigger import Trigger

I18N_DIRNAME = os.path.dirname(os.path.realpath(__file__))
I18N_LOCALES = []
I18N_FILES = []

for f in os.listdir(I18N_DIRNAME):
    i18n_file = os.path.join(I18N_DIRNAME, f)
    if os.path.isfile(i18n_file):
        if re.findall(r"^[a-z]+\_[A-Z]+\.UTF-8\.json$", f):
            _locale = f.split(".json")
            I18N_LOCALES.append({"name": _locale[0], "file": i18n_file})

a_i18n = Ai18n()
a_i18n.locales = [name for name, file in I18N_LOCALES]

for _locale in I18N_LOCALES:
    _name = _locale["name"]
    _file = _locale["file"]
    with open(_file, mode="r", encoding="utf-8") as f:
        data = json.loads(f.read())
        for screen, value in data.items():
            for word, translation in value.items():
                a_i18n.add(k=word, message=translation, module=screen, locale=_name)


# pylint: disable=invalid-name
def T(msg: str, locale: str, module: str):
    """Check if a translation exist and if exist, tranlsate it"""
    found = False
    for loc in I18N_LOCALES:
        name = loc["name"]
        if name == locale:
            found = True

    if not found:
        raise ValueError(f"Locale '{locale}' not found in translations")

    return a_i18n.translate(msg, locale=locale, module=module)

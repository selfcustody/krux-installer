#!/bin/env sh

# download pyinstaller-kivy patch 
PATCHURL="https://raw.githubusercontent.com/ikus060/kivy/21c7110ee79f355d6a42da0a274d2426b1e18665/kivy/tools/packaging/pyinstaller_hooks/__init__.py"
echo "env PATCHURL=$PATCHURL"

PYENV_PATH=`poetry env info --path`
echo "env PYENV_PATH=$PYENV_PATH"

PYENV_VERSION=`python -c 'import sys; t= sys.version_info[:]; print(f"{t[0]}.{t[1]}")'`
echo "env PYENV_VERSION=$PYENV_VERSION"

PYHOOK_PATH="site-packages/kivy/tools/packaging/pyinstaller_hooks/__init__.py"
FULL_PATH=$PYENV_PATH/lib/python$PYENV_VERSION/$PYHOOK_PATH
echo "env FULL_PATH=$FULL_PATH"

wget $PATCHURL -O pyinstaller_hook_patch.py
echo "RUN wget $PATCHURL -O pyinstaller_hook_patch.py"

echo "RUN diff -u $FULL_PATH pyinstaller_hook_patch.py > pyinstaller_hook.patch"
diff -u $FULL_PATH pyinstaller_hook_patch.py > pyinstaller_hook.patch

# patch it
echo "RUN patch $FULL_PATH < pyinstaller_hook.patch"
patch $FULL_PATH < pyinstaller_hook.patch

# remove remaining files
rm pyinstaller_hook_patch.py
echo "RUN rm pyinstaller_hook_patch.py"

rm pyinstaller_hook.patch
echo "RUN rm pyinstaller_hook.patch"

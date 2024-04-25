[String]$PATCHURL = "https://raw.githubusercontent.com/ikus060/kivy/21c7110ee79f355d6a42da0a274d2426b1e18665/kivy/tools/packaging/pyinstaller_hooks/__init__.py"
Write-Verbose "env PATCHURL=$PATCHURL"

[String]$PYENV_PATH = poetry env info --path
Write-Verbose "env PYENV_PATH=$PYENV_PATH"

[String]$PYENV_VERSION = python -c "import sys; t= sys.version_info[:]; print(f'{t[0]}.{t[1]}')"
Write-Verbose "env PYENV_VERSION=$PYENV_VERSION"

[String]$FULL_PATH = "$PYENV_PATH/Lib/site-packages/kivy/tools/packaging/pyinstaller_hooks"
Write-Verbose "env FULL_PATH=$FULL_PATH"

wget $PATCHURL -OutFile pyinstaller_hook_patch.py

Copy-Item pyinstaller_hook_patch.py -Destination "$FULL_PATH"

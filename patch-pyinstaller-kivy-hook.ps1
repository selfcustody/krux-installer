#Requires -Version 7.3

[String]$PATCHURL = "https://raw.githubusercontent.com/ikus060/kivy/21c7110ee79f355d6a42da0a274d2426b1e18665/kivy/tools/packaging/pyinstaller_hooks/__init__.py"
Write-Verbose "env PATCHURL=$PATCHURL"

[String]$PYENV_PATH = poetry env info --path
Write-Verbose "env PYENV_PATH=$PYENV_PATH"

[String]$PYENV_VERSION = python -c 'import sys; t= sys.version_info[:]; print(f"{t[0]}.{t[1]}")'
Write-Verbose "env PYENV_VERSION=$PYENV_VERSION"

[String]$PYHOOK_PATH = "site-packages/kivy/tools/packaging/pyinstaller_hooks/__init__.py"
[String]$FULL_PATH = "$PYENV_PATH/lib/python$PYENV_VERSION/$PYHOOK_PATH"
Write-Verbose "env FULL_PATH=$FULL_PATH"

[String]$GIT_PATH = "C:\Program Files\Git\bin"
Write-Verbose "env GIT_PATH=$GIT_PATH"

Write-Verbose "RUN wget $PATCHURL -OutFile pyinstaller_hook_patch.py"
wget $PATCHURL -OutFile pyinstaller_hook_patch.py

Write-Verbose "RUN $GIT_PATH\diff.exe -u $FULL_PATH pyinstaller_hook_patch.py > pyinstaller_hook.patch"
$GIT_PATH\diff.exe -u $FULL_PATH pyinstaller_hook_patch.py > pyinstaller_hook.patch

Write-Verbose "RUN $GIT\patch.exe $FULL_PATH < pyinstaller_hook.patch"
$GIT_PATH\patch.exe $FULL_PATH < pyinstaller_hook.patch

Write-Verbose "RUN Remove-Item -Path pyinstaller_hook_patch.py"
Remove-Item -Path pyinstaller_hook_patch.py

Write-Verbose "RUN Remove-Item -Path pyinstaller_hook.patch"
Remove-Item -Path pyinstaller_hook.patch

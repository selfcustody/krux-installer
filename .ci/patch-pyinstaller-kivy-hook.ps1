[String]$PATCHURL = "https://raw.githubusercontent.com/ikus060/kivy/21c7110ee79f355d6a42da0a274d2426b1e18665/kivy/tools/packaging/pyinstaller_hooks/__init__.py"
echo "env PATCHURL=$PATCHURL"

[String]$PYENV_PATH = poetry.exe env info --path
echo "env PYENV_PATH=$PYENV_PATH"

[String]$PYENV_VERSION = python -c "import sys; t= sys.version_info[:]; print(f'{t[0]}.{t[1]}')"
echo "env PYENV_VERSION=$PYENV_VERSION"

[String]$FULL_PATH = "$PYENV_PATH\Lib\site-packages\kivy\tools\packaging\pyinstaller_hooks\__init__.py"
echo "env FULL_PATH=$FULL_PATH"

[String]$GIT_TOOLS_PATH = "$Env:PROGRAMFILES\Git\usr\bin"
echo "env GIT_TOOLS_PATH=$GIT_TOOLS_PATH"

[String]$DIFF_PATH = "$GIT_TOOLS_PATH\diff.exe"
echo "env DIFF_PATH=$DIFF_PATH"

[String]$PATCH_PATH = "$GIT_TOOLS_PATH\patch.exe"
echo "env PATCH_PATH=$PATCH_PATH"

[String]$HOOK_PY_PATH = "$pwd\pyinstaller_hook_patch.py"
echo "env HOOK_PY_PATH=$HOOK_PY_PATH"

[String]$HOOK_PATCH_PATH = "$pwd\pyinstaller_hook.patch"
echo "env HOOK_PATCH_PATH=$HOOK_PATCH_PATH"

echo "RUN wget $PATCHURL -OutFile $HOOK_PY_PATH"
wget $PATCHURL -OutFile $HOOK_PY_PATH

echo "RUN '$DIFF_PATH' -u $FULL_PATH $HOOK_PY_PATH | Set-Content $HOOK_PATCH_PATH"
& "$DIFF_PATH" -u $FULL_PATH $HOOK_PY_PATH | Set-Content $HOOK_PATCH_PATH

echo "RUN '$PATCH_PATH' -su -i $HOOK_PATCH_PATH '$FULL_PATH'"
& "$PATCH_PATH" -su -i $HOOK_PATCH_PATH "$FULL_PATH"

echo "RUN Remove-Item -Path $HOOK_PY_PATH"
Remove-Item -Path $HOOK_PY_PATH

echo "RUN Remove-Item -Path $HOOK_PATCH_PATH"
Remove-Item -Path $HOOK_PATCH_PATH

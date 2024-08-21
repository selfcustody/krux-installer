# Build process for pyinstaller/kivy
# will require some editions and, do it mannually
# is something impossible on github actions
# so we do it as script
# see more at
# https://kivy.org/doc/stable/guide/packaging-windows.html

# Now we need to edit the spec file to add the dependencies hooks to correctly build the exe.
# Open the spec file with your favorite editor and add these lines at the beginning of the spec
$header = "# -*- mode: python ; coding: utf-8 -*-"
$new_header = "# -*- mode: python ; coding: utf-8 -*-`r`nfrom kivy_deps import sdl2, glew"

# which we will edit to add the dependencies. 
# In this instance, edit the arguments to the EXE command
$old_code = @"
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='krux-installer',
"@

$new_code = @"
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
    name='krux-installer',
"@

# Now do the .spec edition and build the .exe
(Get-Content -Raw .\krux-installer.spec).replace($header, $new_header).replace($old_code, $new_code) | Set-Content .\krux-installer.spec
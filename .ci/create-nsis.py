# Miscelanious code from
# https://github.com/Thiagojm/NSIS-Script-Maker-for-Windows-/blob/main/nsis_template.txt
# https://gist.github.com/mattiasghodsian/a30f50568792939e35e93e6bc2084c2a
import os
import re
import platform
from argparse import ArgumentParser, Namespace
from sys import set_coroutine_origin_tracking_depth

parser = ArgumentParser(
    prog='create-nsis',
    description='Create a Setup installer for your program',
    usage="create-nsis [...options] | Out-File -FilePath <path> -Encoding utf8 "
)

parser.add_argument("-a", "--name", help="The name of your app")
parser.add_argument("-b", "--binary", help="The path of your app")
parser.add_argument("-o", "--organization", help="The name of your organization")
parser.add_argument("-d", "--description", help="The application description")
parser.add_argument("-V", "--app-version", help="The version of your application o x.y.z form")
parser.add_argument("-l", "--license", help="The path of your application license")
parser.add_argument("-i", "--icon", help="The icon path of your application")
parser.add_argument("-I", "--asset", action="append", help="The name of asset and the path in form of name:path")
parser.add_argument("-O", "--output", help="The folder where the the NSIS script will be put")

def escape(message: str) -> str:
    if platform.system() == "Windows":
        return message.replace("/", "\\")
    else:
        return message

def make_headers(args: Namespace) -> str:
    print("* make headers")
    return "\n".join([
        ";--------------------------------",
        "!define MULTIUSER_EXECUTIONLEVEL Highest",
        "!define MULTIUSER_MUI",
        "",
        ";---------------------------------",
        "; Main header",
        "!include \"MultiUser.nsh\"",
        "!include \"MUI2.nsh\"",
        "",
        ""
    ])

def make_defines(args: Namespace) -> str:
    print("* make defines")
    version = args.app_version.split(".")
    binary = escape(args.binary)
    license = escape(args.license)
    icon = escape(args.icon)
    install_size = os.path.getsize(args.binary)
    install_size += os.path.getsize(args.icon)
    install_size += os.path.getsize(args.license)

    text = [
        ";--------------------------------",
        "; Custom define",
        f"!define APP_NAME {args.name}",
        f"!define ORG_NAME {args.organization}",
	    f"!define APP_DESC \"{args.description}\"",
	    f"!define APP_BINARY \"{binary}\"",
	    f"!define APP_VERSION_MAJOR {version[0]}",
	    f"!define APP_VERSION_MINOR {version[1]}",
	    f"!define APP_VERSION_BUILD {version[2]}",
	    f"!define APP_SLUG \"{args.name} v{args.app_version}\"",
        f"!define APP_LICENSE \"{license}\"",
        f"!define APP_ICON \"{icon}\"",
    ]

    if args.asset is not None and len(args.asset) > 0:
        for asset in args.asset:
            _asset = asset.split(":")
            _asset_name = _asset[0]
            _asset_rev = escape(_asset[1])
            text.append(f"!define APP_ASSET_{_asset_name.upper()} \"{_asset_rev}\"")

    text.append("")
    text.append("")
    return "\n".join(text)

def make_general(args: Namespace) -> str:
    print("* make general")
    return "\n".join([
        ";--------------------------------",
        "; General",
        "Name \"${APP_NAME}\"",
        "OutFile \"${APP_NAME} Setup.exe\"",
        "InstallDir \"$PROGRAMFILES\\${APP_NAME}\"",
        "LicenseData \"${APP_LICENSE}\"",
        "InstallDirRegKey HKCU \"Software\\${APP_NAME}\" \"\"",
        "RequestExecutionLevel admin",
        "Unicode true",
        #"SilentInstall silent",
        "",
        ""
    ])

def make_ui(args: Namespace) -> str:
    print("* make UI")
    return "\n".join([
        ";--------------------------------",
        "; UI",
        "!define MUI_ICON \"${APP_ICON}\"",
        #"!define MUI_HEADERIMAGE",
        #"!define MUI_WELCOMEFINISHPAGE_BITMAP \"assets\\logo.png\"",
        #"!define MUI_HEADERIMAGE_BITMAP \"assets\\logo.png\"",
        "!define MUI_ABORTWARNING",
        "!define MUI_WELCOMEPAGE_TITLE \"${APP_SLUG} Setup\"",
        "",
        ""
    ])

def make_pages(args: Namespace) -> str:
    print("* make pages")
    return "\n".join([
        ";--------------------------------",
        "; Pages",
        "!define MUI_FINISHPAGE_SHOWREADME \"\"",
        "!define MUI_FINISHPAGE_SHOWREADME_NOTCHECKED",
        "!define MUI_FINISHPAGE_SHOWREADME_TEXT \"Create Desktop/Menu entry shortcuts\"",
        "!define MUI_FINISHPAGE_SHOWREADME_FUNCTION finishpageaction",
        "!insertmacro MUI_PAGE_WELCOME",
        "!insertmacro MULTIUSER_PAGE_INSTALLMODE",
        "!insertmacro MUI_PAGE_LICENSE \"LICENSE\"",
        "!insertmacro MUI_PAGE_COMPONENTS",
        "!insertmacro MUI_PAGE_DIRECTORY",
        "!insertmacro MUI_PAGE_INSTFILES",
        "!insertmacro MUI_PAGE_FINISH",
        "!insertmacro MUI_UNPAGE_CONFIRM",
        "!insertmacro MUI_UNPAGE_INSTFILES",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Welcome to ${APP_SLUG} setup\"",
        "!insertmacro MUI_LANGUAGE \"English\"",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Bem vindo à cconfiguração do ${APP_SLUG}\"",
        "!insertmacro MUI_LANGUAGE \"Portuguese\"",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Bienvenido a la configuración de ${APP_SLUG}\"",
        "!insertmacro MUI_LANGUAGE \"Spanish\"",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Benvenuto nell'installazione di ${APP_SLUG}\"",
        "!insertmacro MUI_LANGUAGE \"Italian\"",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Bienvenue dans la configuration de ${APP_SLUG}\"",
        "!insertmacro MUI_LANGUAGE \"French\"",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Welkom by ${APP_SLUG} Setup\"",
        "!insertmacro MUI_LANGUAGE \"Afrikaans\"",
        "!define MUI_TEXT_WELCOME_INFO_TITLE \"Добро пожаловать в ${APP_SLUG} Конфигурация\"",
        "!insertmacro MUI_LANGUAGE \"Russian\"",
        "",
        ""
    ])

def make_macro_verify_user_is_admin(args: Namespace) -> str:
    print("* make macro VerifyUserIsAdmin")
    return "\n".join([
        ";--------------------------------",
        "; Macro verify user is admin",
        "!include LogicLib.nsh",
        "!macro VerifyUserIsAdmin",
        "UserInfo::GetAccountType",
        "pop $0",  
        ";Require admin rights on NT4+",
        "${If} $0 != \"admin\"",
        "\tmessageBox mb_iconstop \"Administrator rights required!\"",
        "\t;ERROR_ELEVATION_REQUIRED",
        "\tsetErrorLevel 740",
        "\tquit",
        "${EndIf}",
        "!macroend",
        "",
        ""
    ])

def make_on_init(args: Namespace) -> str:
    print("* make function onInit")
    return "\n".join([
        ";--------------------------------",
        "; function on init",
        "function .onInit",
        "\tsetShellVarContext all",
        "\t!insertmacro VerifyUserIsAdmin",
        "\t!insertmacro MULTIUSER_INIT",
        "functionEnd",
        "",
        ""
    ])

def make_finish_page_action(args: Namespace) -> str:
    print("* make function finishpageaction")
    # Extract just the filename from the binary path for the shortcut target
    binary_filename = os.path.basename(args.binary)
    return "\n".join([
        ";--------------------------------",
        "; function finishpageaction",
        "function finishpageaction",
        "\t; Start Menu",
        "\tCreateDirectory \"$SMPROGRAMS\\${APP_NAME}\"",
        f"\tCreateShortCut  \"$SMPROGRAMS\\${{APP_NAME}}.lnk\" \"$INSTDIR\\{binary_filename}\"",
        "",
        "\t; Desktop shortcut",
        f"\tCreateShortCut  \"$DESKTOP\\${{APP_NAME}}.lnk\" \"$INSTDIR\\{binary_filename}\"",
        "functionEnd",
        "",
        "",
    ])

def make_install_section(args: Namespace) -> str:
    print("* make install section")
    text = ""
    text += "\n".join([
        ";--------------------------------",
        "; Section - Install App",
        "Section \"install\" SEC_01",
        #"\tSection \"-hidden install\"",
        "\tSectionIn RO",
        "\tSetOutPath \"$INSTDIR\"",
        "",
        "\t; Files added here should be removed by the uninstaller (see section 'uninstall')",
        "\tFile /r \"${APP_BINARY}\"",
    ])

    _text = []
    
    if args.asset is not None and len(args.asset) > 0:
        for asset in args.asset:
            _asset = asset.split(":")
            _asset_name = _asset[0].upper()
            _text.append("\tFile /r \"${APP_ASSET_" +_asset_name + "}\"")

    text += "\n".join(_text)

    text += "\n".join([
        "\t; Uninstaller - See function un.onInit and section 'uninstall' for configuration",
        "\tWriteUninstaller \"$INSTDIR\\uninstall.exe\"",
        "",
        "\t; Registry information for add/remove programs",
        "\tWriteRegStr HKCU \"Software\\${APP_NAME}\" \"\" $INSTDIR",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"DisplayName\" \"${APP_NAME} - ${APP_DESC}\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"UninstallString\" \"$\\\"$INSTDIR\\uninstall.exe$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"QuietUninstallString\" \"$\\\"$INSTDIR\\uninstall.exe$\\\" /S\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"InstallLocation\" \"$\\\"$INSTDIR$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"DisplayIcon\" \"$\\\"$INSTDIR\\${APP_ICON}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"Publisher\" \"$\\\"${ORG_NAME}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"DisplayVersion\" \"$\\\"${APP_VERSION_MAJOR}.${APP_VERSION_MINOR}.${APP_VERSION_BUILD}$\\\"\"",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"VersionMajor\" ${APP_VERSION_MAJOR}",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"VersionMinor\" ${APP_VERSION_MINOR}",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"VersionMinor\" ${APP_VERSION_MINOR}",
        "",
        "\t; There is no option for modifying or repairing the install",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"NoModify\" 1",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"NoRepair\" 1",
        "",
        "\t; Write MULTIUSER_INSTALLMODE_DEFAULT_REGISTRY_VALUENAME so the correct context can be detected in the uninstaller.",
        "\tWriteRegStr ShCtx \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" $MultiUser.InstallMode 1",
        "",
        "\t; Obtain the size of the files, in kilobytes, in section SEC_01",
        "\tSectionGetSize \"${SEC_01}\" $0",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}\" \"EstimatedSize\" $0",
        "",
        "\tWriteUninstaller \"$INSTDIR\\Uninstall.exe\"",
        "SectionEnd",
        "",
        ""

    ])

    return text

def make_uninstaller(args: Namespace) -> str:
    print("* make uninstaller section")
    return "\n".join([
        ";--------------------------------",
        "; Uninstaller",
        "function un.onInit",
        "\tSetShellVarContext all",
        "\t; Verify the uninstaller - last chance to back out",
        "\tMessageBox MB_OKCANCEL \"Permanantly remove ${APP_NAME}?\" IDOK next",
        "\t\tAbort",
        "\tnext:",
        "\t!insertmacro VerifyUserIsAdmin",
        "\t!insertmacro MULTIUSER_UNINIT",
        "functionEnd",
        "",
        ";--------------------------------",
        "; Uninstall section",
        "Section \"uninstall\"",
        "",
        "",
        "\t; Delete menu  entries",
        "\tDelete \"$SMPROGRAMS\\${APP_NAME}.lnk\"",
        "\tRmDir /r \"$SMPROGRAMS\\${APP_NAME}\"",
        "",
        "\t; Delete desktop shortcut",
        "\tDelete \"$DESKTOP\\${APP_NAME}.lnk\"",
        "",
        "\t; Remove files",
        "\tDelete $INSTDIR\\*",
        "\tDelete $INSTDIR\\uninstall.exe",
        "",
        "\t; Try to remove the install directory - this will only happen if it is empty",
        "\tRmDir /r $INSTDIR",
        "",
        "\t; Remove uninstaller information from the registry",
        "\tDeleteRegKey HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\"",
        "sectionEnd"
    ])

args = parser.parse_args()

try:
    file = os.path.join(args.output, f"{args.name}.nsi")
    
    with open(file, mode="w", encoding="utf-8") as nsis_script:
        nsis_script.write(make_headers(args))
        nsis_script.write(make_defines(args))
        nsis_script.write(make_general(args))
        nsis_script.write(make_ui(args))
        nsis_script.write(make_macro_verify_user_is_admin(args))
        nsis_script.write(make_finish_page_action(args))
        nsis_script.write(make_on_init(args))
        nsis_script.write(make_pages(args))
        nsis_script.write(make_install_section(args))
        nsis_script.write(make_uninstaller(args))
        
    print(f"{file} created")

except Exception as err:
    print(err)

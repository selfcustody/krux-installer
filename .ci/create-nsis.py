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
parser.add_argument("-H", "--help-url", help="The application help URL")
parser.add_argument("-u", "--update-url", help="The application update url")
parser.add_argument("-A", "--about-url", help="The application about URL")
parser.add_argument("-i", "--icon", help="The icon path of your application")
parser.add_argument("-I", "--asset", action="append", help="The name of asset and the path in form of name:path")

def escape(message: str) -> str:
    if platform.system() == "Windows":
        return message.replace("/", "\\")
    else:
        return message

def make_headers(args: Namespace) -> str:
    return "\n".join([
        ";--------------------------------",
        "; Main header",
        "!include \"MUI2.nsh\"",
        "",
        ""
    ])

def make_defines(args: Namespace) -> str:
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
	    f"!define APP_DESC {args.description}",
	    f"!define APP_BINARY \"{binary}\"",
	    f"!define APP_VERSION_MAJOR {version[0]}",
	    f"!define APP_VERSION_MINOR {version[1]}",
	    f"!define APP_VERSION_BUILD {version[2]}",
	    f"!define APP_SLUG \"{args.name} v{args.app_version}\"",
        f"!define APP_HELP_URL \"{args.help_url}\"",
        f"!define APP_UPDATE_URL \"{args.help_url}\"",
        f"!define APP_ABOUT_URL \"{args.about_url}\"",
        f"!define APP_LICENSE \"{license}\"",
        f"!define APP_ICON \"{icon}\"",
    ]

    if args.asset is not None and len(args.asset) > 0:
        for asset in args.asset:
            _asset = asset.split(":")
            _asset_name = _asset[0]
            _asset_rev = escape(_asset[1])
            install_size += os.path.getsize(_asset_rev)
            text.append(f"!define APP_ASSET_{_asset_name.upper()} \"{_asset_rev}\"")

    text.append(f"!define APP_INSTALL_SIZE {install_size}")
    text.append("")
    text.append("")
    return "\n".join(text)

def make_general(args: Namespace) -> str:
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
    return "\n".join([
        ";--------------------------------",
        "; Pages",
        "!insertmacro MUI_PAGE_WELCOME",
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
    return "\n".join([
        ";--------------------------------",
        "; function on init",
        "function .onInit",
        "\tsetShellVarContext all",
        "\t!insertmacro VerifyUserIsAdmin",
        "functionEnd",
        "",
        ""
    ])

def make_install_section(args: Namespace) -> str:
    text = ""
    text += "\n".join([
        ";--------------------------------",
        "; Section - Install App",
        "Section \"install\"",
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
        "",
        "",
        "\t; Start Menu",
        "\tCreateDirectory \"$SMPROGRAMS\\${APP_NAME}\"",
        "\tCreateShortCut \"$SMPROGRAMS\\${ORG_NAME}\\${APP_NAME}.lnk\" \"$INSTDIR\\${APP_NAME}.exe\" \"\" \"$INSTDIR\\${APP_ICON}\"",
        "",
        ""
    ])

    text += "\n".join([
        "\t; Uninstaller - See function un.onInit and section 'uninstall' for configuration",
        "\tWriteUninstaller \"$INSTDIR\\uninstall.exe\"",
        "",
        "\t; Registry information for add/remove programs",
        "\tWriteRegStr HKCU \"Software\\${APP_NAME}\" \"\" $INSTDIR",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"DisplayName\" \"${ORG_NAME} - ${APP_NAME} - ${APP_DESC}\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"UninstallString\" \"$\\\"$INSTDIR\\uninstall.exe$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"QuietUninstallString\" \"$\\\"$INSTDIR\\uninstall.exe$\\\" /S\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"InstallLocation\" \"$\\\"$INSTDIR$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"DisplayIcon\" \"$\\\"$INSTDIR\\${APP_ICON}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"Publisher\" \"$\\\"${ORG_NAME}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"HelpLink\" \"$\\\"${APP_HELP_URL}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"URLUpdateInfo\" \"$\\\"${APP_UPDATE_URL}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"URLInfoAbout\" \"$\\\"${APP_ABOUT_URL}$\\\"\"",
        "\tWriteRegStr HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"DisplayVersion\" \"$\\\"${APP_VERSION_MAJOR}.${APP_VERSION_MINOR}.${APP_VERSION_BUILD}$\\\"\"",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"VersionMajor\" ${APP_VERSION_MAJOR}",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"VersionMinor\" ${APP_VERSION_MINOR}",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"VersionMinor\" ${APP_VERSION_MINOR}",
        "",
        "\t; There is no option for modifying or repairing the install",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"NoModify\" 1",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"NoRepair\" 1",
        "",
        "\t; Set the INSTALLSIZE constant (!defined at the top of this script) so Add/Remove Programs can accurately report the size",
        "\tWriteRegDWORD HKLM \"Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${ORG_NAME} ${APP_NAME}\" \"EstimatedSize\" ${APP_INSTALL_SIZE}",
        "\tWriteUninstaller \"$INSTDIR\\Uninstall.exe\"",
        "SectionEnd",
        "",
        ""

    ])

    return text

def make_uninstaller(args: Namespace) -> str:
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
        "functionEnd",
        "",
        ";--------------------------------",
        "; Uninstall section",
        "Section \"uninstall\"",
        "",
        "\t; Remove Start Menu launcher",
        "\tDelete \"$SMPROGRAMS\\${ORG_NAME}\\${APP_NAME}.lnk\"",
        "",
        "\t; Try to remove the Start Menu folder - this will only happen if it is empty",
        "\tRmDir \"$SMPROGRAMS\\${ORG_NAME}\"",
        "",
        "\t; Remove Desktop Shortcut",
        "\tDelete \"DESKTOP\\${APP_NAME}.lnk\"",
        "",
        "\t; Remove files",
        "\tDelete $INSTDIR\\*",
        "\tRmDir /r $INSTDIR\\",
        "",
        "\t; Always delete uninstaller as the last action",
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
script = make_headers(args)
script += make_defines(args)
script += make_general(args)
script += make_ui(args)
script += make_macro_verify_user_is_admin(args)
script += make_on_init(args)
script += make_pages(args)
script += make_install_section(args)
script += make_uninstaller(args)
print(script)

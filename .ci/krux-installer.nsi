
/*=== !include "MUI.nsh" ; -use only to set custom icon ===*/
/*=== !define MUI_ICON "${NSISDIR}\Contrib\Icons\Youriconname.ico ===*/

RequestExecutionLevel admin ;
Unicode true
SilentInstall silent

;--------------------------------
; Custom defines
	!define NAME "krux-installer"
	!define APPFILE "${NAME}.exe"
	!define VERSION "0.2.0"
	!define SLUG "${NAME} v${VERSION}"

;--------------------------------
; General
	Name "${NAME}"
	OutFile "${NAME} Setup.exe"
	InstallDir "$PROGRAMFILES\${NAME}"
	InstallDirRegKey HKCU "Software\${NAME}" ""
	RequestExecutionLevel admin
	Unicode true
	SilentInstall silent

;--------------------------------
; UI
	!define MUI_ICON "assets\icon.ico"
	!define MUI_HEADERIMAGE
	!define MUI_WELCOMEFINISHPAGE_BITMAP "assets\logo.bmp"
	!define MUI_HEADERIMAGE_BITMAP "assets\icon.bmp"
	!define MUI_ABORTWARNING
	!define MUI_WELCOMEPAGE_TITLE "${SLUG} Setup"

;--------------------------------
; Pages
	; Installer pages
	!insertmacro MUI_PAGE_WELCOME
	!insertmacro MUI_PAGE_LICENSE "LICENSE"
	!insertmacro MUI_PAGE_COMPONENTS
	!insertmacro MUI_PAGE_DIRECTORY
	!insertmacro MUI_PAGE_INSTFILES
	!insertmacro MUI_PAGE_FINISH
	
	; Uninstaller pages
	!insertmacro MUI_UNPAGE_CONFIRM
	!insertmacro MUI_UNPAGE_INSTFILES
  
	; Set UI language
  	!insertmacro MUI_LANGUAGE "English"

;--------------------------------
; Section - Install App

  Section "-hidden app"
    SectionIn RO
    SetOutPath "$INSTDIR"
    File /r "app\*.*" 
    WriteRegStr HKCU "Software\${NAME}" "" $INSTDIR
    WriteUninstaller "$INSTDIR\Uninstall.exe"
  SectionEnd

# CHANGELOG

## 0.0.20

- Fixed Fedora crashes;
- Better error handling during flash procedure;
- Better error handling during wipe procedure;
- Better error handling during air-gap update procedure;

## 0.0.20-beta

- Now user can, after download and verify an official firmware, select between:
  - to flash;
  - or make an airgapped update:
    - user will be requested to insert a SDCard on computer;
    - user can select among recognized removable drives;
    - both firmware.bin and firmware.bin.sig will be copied to sdcard;
    - after the copy, user will be requested to eject sdcard and insert it on device;
    - at same time, the firmware.bin's computed hash will appear to compare with the computed hash on device;

- Minor updates
  - added support to de_DE locale;
  - added support to ja_JP locale;
  - fixes on Windows bug that didn't allow users to select a custom asset folder;

## 0.0.20-alpha-3

- Fix the bug that crash when a new firmware version is added on `selfcustody/krux`, but not it isnt a valid one in `VALID_DEVICES_VERSIONS`;
- The fix suggested by @odudex to manage new versions (good when a hot fix is made) in line 101 of `src/app/screens/select_device_screen.py`;

## 0.0.20-alpha-2

- Changed the version from `0.0.2-alpha` to `0.0.20-alpha-2` as suggested by @odudex;
- Refactored the code a little bit to be more pythonic;
- Removed startup messages as suggested by @tadeubas:
  - On linux the `GreetingsScreen` class will check:
    - if user is on `dialout`/`uucp` group (debian and fedora based / archlinux);
    - internet connection
  - On MacOS an Windows the `GreetingsScreen` class will check:
    - internet connection
- Added the window resize behaviour;
- Removed fullscreen on startup;
- Fedora and Ubuntu:
  - fixed desktop icon entry on `.ci/create-deb`;
  - fixed desktop icon entry on `.ci/create-rpm`;
- Added more tests:
  - ask_permissions_dialout_screen;
  - error_screen.

## 0.0.2-alpha

- code refactoration from `nodejs` to `python`;
- re-build project from `electron` to `kivy`;
- Support for MacOS (arm64 and intel processors);
- Support to download older versions;
- Support to devices according to the appropriate version:
  - M5stickV;
  - Amigo;
  - Dock;
  - Bit;
  - Yahboom;
  - Cube;
- Flash made with the `ktool` from its source;
- Wipe made with the `ktool` from its source;
- Added settings page:
  - Enable change path of downloaded assets;
  - Enable change of flash baudrate;
  - Enable change of locale;
- Added about page
- Locale support for 10 languages:
  - af_ZA (South Africa Afrikaans);
  - en_US (USA English);
  - es_ES (Spain spanish);
  - fr_FR (France french);
  - it_IT (Italian);
  - ko_KR (South Korean korean);
  - nl_NL (Netherlands dutch);
  - pt_BR (Brazilian portuguese);
  - ru_RU (Russian cyrillic);
  - zh_CN (Simplified chinese)
  
## 0.0.1

- Major updates dependencies:
  - `electron`: 28.1.0;
  - `vite-plugin-electron`: 0.15.5;
  - `wdio-electron-service`: 6.0.2.
- Minor updates:
  - `@wdio/cli`: 8.27.0;
  - `@wdio/globals`: 8.27.0;
  - `@wdio/local-runner`: 8.27.0;
  - `@wdio/mocha-framework`: 8.27.0;
  - `@wdio/spec-reporter`: 8.27.0;
  - `vue`: 3.3.13;
  - `vue-tsc`: 1.8.26;
  - `vuetify`: 3.4.8;
- Refactored `test/e2e/specs`:
  - to suit `wdio-electron-service` major updates that break E2E tests;
  - renamed extensions to `mts` to suit `vite-plugin-electron`;
  - updated krux firmware version checks to `23.09.1`;
- Updated `openssl` for windows to `3.2.0` *;
- Removed MacOS release since the current approach did not worked well on MacOS;

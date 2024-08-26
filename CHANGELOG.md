# CHANGELOG

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

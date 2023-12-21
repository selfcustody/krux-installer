# 0.0.1

- Updated main dependencies:
  - `electron`: 28.0.0;
  - `vite-plugin-electron`: 0.15.5;
  - `wdio-electron-service`: 6.0.2.

- Refactored `test/e2e/specs`:
  - to suit `wdio-electron-service` major updates that break E2E tests;
  - renamed extensions to `mts` to suit `vite-plugin-electron`;
  - updated krux firmware version checks to `23.09.1`.

- Updated `openssl` for windows to `3.2.0`.

- Removed MacOS release since the current approach did not worked well
  on MacOS;

**Disclaimer**:  
> We will replace the development to python/kivy due to
two different situations: (1) Windows: needs a custom compilation of openssl
and  `electron` use `boringssl`; with a python release, it's possible to use
krux python modules inside the application, so the krux team envisioned
better compatibility between linux, windows and mac without inject an `opeessl`
binary in windows; (2) some extended permissions in MacOS and/or the lack
of an Apple ID linked to the software on darwin system do not allow the flash feature.

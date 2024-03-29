# 0.0.1

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

> \* see [WARNING](WARNING.md)

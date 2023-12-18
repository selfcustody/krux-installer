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

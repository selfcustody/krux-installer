# Warning

We will replace the development of `krux-installer` from `typescript/electron`
to `python/kivy`.

## Why the change?

The decision was made among the members of the `selfcustody`
team for the following reasons:

- To unify software development in Python;
- Behaviors with SSL routines, in windows,
  that differ from what would be considered "normalized";
- Failure to flash in MacOS.

### Why unify software development in Python

Maintenance and review of code can be more extensive.

### What systems differ in behavior with SSL routines?

- Windows
- MacOS

### Why we need SSL routines?

When downloading official krux firmware versions, it is necessary to verify
the signature through an external OpenSSL tool, as a way to verify the authenticity
of the downloaded binaries.

## Why behaviors with SSL routines differ?

We need to pack an external `openssl` into `krux-installer` package.

### Why?

On "Unix like" releases (Linux and MacOS), verification is easily done
since such tool exists natively in the operating system.
In windows release, we are faced with the peculiarity of the operating
system in question.  Windows does not natively have such a tool
(see this [issue](https://github.com/qlrd/krux-installer/issues/2)).

### How has it been resolved so far?

We compiled a stable version of OpenSSL from the
[source](https://github.com/openssl/openssl) and packaged it on our software.

#### This isn't insecure?

We believe not, since the compilation process
is done entirely in a reproducible virtual environment and,
therefore, not locally, with the github-action
[compile-openssl-windows-action](https://github.com/qlrd/compile-openssl-windows-action/actions).

## MacOS: how flash fails?

The application works until you try to flash the device. Once you try
to flash, a message like this will appear:

```bash
Error: 0:336: execution error: [1047] Cannot open PyInstaller
archive from executable
(/Users/user/Documents/krux-installer/krux-v23.09.0/ktool-mac)
or external archive
(/Users/user/Documents/krux-installer/krux-v23.09.0/ktool-mac.pkg) (255)

    at Socket. (/Applications/krux-installer.app/Contents/Resources/app.asar/dist-electron/main/index.js:6:381)
    at Socket.emit (node:events:513:28)
    at addChunk (node:internal/streams/readable:324:12)
    at readableAddChunk (node:internal/streams/readable:297:9)
    at Socket.push (node:internal/streams/readable:234:10)
    at Pipe.onStreamRead (node:internal/stream_base_commons:190:23)
```

### What this means?

This means that the `ktool-mac`, aka the "flasher",
in `krux-installer` failed to be executed.

### Why this happen?

Although we don't know for sure, we suspect that:

- (1) The `krux-installer` download `ktool-mac` from a source
that `apple` did not recognize as "safe";
- (2) If it isn't "safe", `macOS` adds an [extended file permission](https://apple.stackexchange.com/questions/42177/what-does-signify-in-unix-file-permissions);
- (3) This extended file permission puts the `ktool-mac` in a quarantine;
- (4) flash will not work.

## And why not use a nodejs module, instead an external tool, to verify?

The usage of SSL routines, in nodejs is done by
[Native Node Modules](https://www.electronjs.org/docs/latest/tutorial/using-native-node-modules).

### And?

As stated by `electron` documentation:

> Native Node.js modules are supported by Electron,
but since Electron has a different application binary interface (ABI)
from a given Node.js binary (due to **differences such as using Chromium's
BoringSSL instead of OpenSSL**)

### What's BoringSSL?

As stated by BoringSSL [`README`](https://github.com/google/boringssl):

> BoringSSL is a fork of OpenSSL that is designed to meet Google's needs.

### How BoringSSL affects krux-installer?

The [curve used](https://github.com/selfcustody/krux/blob/7add64a0fa8cdae65e49f8bd9bd0f7ff09e95e84/krux#L151)
to sign the firmware is `secp256k1` (the same used in Bitcoin).

The BoringSSL [does not implement
`secp256k1`](https://github.com/electron/electron/issues/32535) and,
therefore, it is not possible
to check this curve using javascript code in electron.

## These can be solved with a python module?

Yes, we believe so;

### Which module?

[pyOpenSSL](https://pypi.org/project/pyOpenSSL/);

### And why do you believe that?

We've already made an experiment with
[`krux-file-signer`](https://github.com/selfcustody/krux-file-signer/blob/c541dbc730f833d64c068245fae30a42bc3f2580/src/cli/verifyer.py#L97)
in linux and windows.

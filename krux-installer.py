# The MIT License (MIT)

# Copyright (c) 2021-2024 Krux contributors

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
krux-installer.py
"""

import re
import sys

REG_CLI = r"^(.*krux-installer)(\.py)?(.*)$"

if not re.findall(REG_CLI, " ".join(sys.argv)):
    print("Reserved to run kivy app")

if re.findall(REG_CLI, " ".join(sys.argv)):

    import os
    import tempfile
    from argparse import ArgumentParser
    from src.utils.constants import get_name, get_version, get_description
    from src.utils.selector import Selector, VALID_DEVICES
    from src.utils.downloader import (
        ZipDownloader,
        Sha256Downloader,
        SigDownloader,
        PemDownloader,
        BetaDownloader,
    )
    from src.utils.verifyer import (
        Sha256Verifyer,
        Sha256CheckVerifyer,
        SigVerifyer,
        SigAnyVerifyer,
        SigCheckVerifyer,
        PemCheckVerifyer,
    )
    from src.utils.unzip import KbootUnzip, FirmwareUnzip
    from src.utils.flasher import Flasher, Wiper
    from src.utils.signer import CliSigner

    parser = ArgumentParser(prog=get_name(), description=get_description())

    if sys.platform in ("linux", "darwin", "freebsd", "win32"):
        parser.add_argument("-v", "--version", help="Show version", action="store_true")
        parser.add_argument(
            "-a",
            "--available-firmwares",
            help="Show available versions (require internet connection)",
            action="store_true",
        )
        parser.add_argument(
            "-A",
            "--available-devices",
            help="Show available devices",
            action="store_true",
        )
        parser.add_argument("-d", "--device", help="Select a device to be flashed")
        parser.add_argument(
            "-f", "--firmware", help="Select a firmware version to be flashed"
        )
        parser.add_argument(
            "-D",
            "--destdir",
            help="Directory where assets will be stored (default: OS tmpdir)",
            default=tempfile.gettempdir(),
        )
        parser.add_argument(
            "-F",
            "--flash",
            help=" ".join(
                [
                    "If set, download the kboot.kfpkg firmware and flash.",
                    "Otherwise, download firmware.bin and store in destdir",
                ]
            ),
            action="store_true",
        )
        parser.add_argument(
            "-w",
            "--wipe",
            help=" ".join(
                [
                    "Erase all device's data and firmware (CAUTION: this will make",
                    "the device unable to work until you install a new firmware)",
                ]
            ),
            action="store_true",
        )
        parser.add_argument(
            "-s", "--sign", help=" ".join(["sign a file with your device"])
        )

        parser.add_argument(
            "-S",
            "--save-hash",
            action="store_true",
            help=" ".join(["save a sha256.txt file when signing with your device"]),
        )

        
        parser.add_argument(
            "-V", "--verify", help=" ".join(["verify the authenticity of a signature file (.sig) signed with krux"])
        )

        
        parser.add_argument(
            "-K", "--filename", help=" ".join(["the file to be verified with --verify option"])
        )
        
        parser.add_argument(
            "-p", "--pubkey", help=" ".join(["the public key certificate (.pem) to be verified with --verify option"])
        )

    else:
        raise RuntimeError(f"Not implementated for {sys.platform}")

    args = parser.parse_args()

    if args.version:
        print(get_version())

    elif args.available_firmwares:
        selector = Selector()
        for version in selector.releases:
            print(f"* {version}")

    elif args.available_devices:
        for device in VALID_DEVICES[1 : len(VALID_DEVICES)]:
            print(f"* {device}")

    elif args.wipe and not args.device:
        raise RuntimeError("--wipe must be paired with --device option")

    elif args.wipe and args.device:
        print(
            "🔥 Wiping firmware and data. Please be patient and wait until process finish."
        )
        w = Wiper()
        w.wipe(device=args.device)

    elif args.sign:
        signer = CliSigner(filename=args.sign)
        signer.print_scan_hash_message()
        signer.make_hash()
        signer.print_hash()
        if args.save_hash:
            signer.save_hash()

        signer.print_scan_signature_message()
        signer.make_signature()
        signer.save_signature()

        signer.print_scan_pubkey_message()
        signer.make_pubkey()
        signer.save_pubkey()

    elif args.verify:
        if not args.filename and not args.pubkey:
            raise RuntimeError("--verify [FILE].sig must be paired with --filename [FILE] and --pubkey [FILE].pem")
        
        sig_check_verifyer = SigCheckVerifyer(filename=args.verify)
        pem_check_verifyer = PemCheckVerifyer(filename=args.pubkey)
        sig_check_verifyer.load()
        pem_check_verifyer.load()
        sig_verifyer = SigAnyVerifyer(
            filename=args.filename,
            signature=sig_check_verifyer.data,
            pubkey=pem_check_verifyer.data,
        )
        sig_verifyer.load()
        
        result = sig_verifyer.verify()

        if not result:
            raise RuntimeError("Invalid signature")
        
        print("✅ Signature Verified Successfully")

    elif args.device and not args.firmware:
        raise RuntimeError("--device must be paired with --firmware option")

    elif args.device and args.firmware:
        FIRMWARE_NAME = ""
        ZIPFILE = ""
        answer = ""

        def download_zip():
            """Download zip release and prints message"""
            print()
            print(f"⚡ Downloading {args.destdir}/krux-{args.firmware}.zip release")
            zipd = ZipDownloader(version=args.firmware, destdir=args.destdir)
            return zipd.download()

        def download_zip_sha256sum():
            """Download zip.sha256.txt release and prints message"""
            print()
            print(f"⚡ Downloading {args.destdir}/krux-{args.firmware}.zip.sha256.txt")
            sha256 = Sha256Downloader(version=args.firmware, destdir=args.destdir)
            return sha256.download()

        def download_zip_sig():
            """Download zip.sig release and prints message"""
            print()
            print(f"⚡ Downloading {args.destdir}/krux-{args.firmware}.zip.sig")
            sig = SigDownloader(version=args.firmware, destdir=args.destdir)
            return sig.download()

        def download_pem():
            """Download selfcustody's public key certificate and prints message"""
            print()
            print(f"⚡ Downloading {args.destdir}/selfcustody.pem")
            pem = PemDownloader(destdir=args.destdir)
            return pem.download()

        def verify_sha256sum(filename: str):
            """Make sha256sum of .zip release and check it against the .sha256.txt file"""
            print()
            print(f"⚠  Verifying {filename}.zip with {filename}.sha256.txt")
            sha256_check_verifyer = Sha256CheckVerifyer(
                filename=f"{filename}.sha256.txt"
            )
            sha256_verifyer = Sha256Verifyer(filename=filename)
            sha256_check_verifyer.load()
            sha256_verifyer.load()
            print(f"sha256sum: {sha256_verifyer.data}")
            print(f"expected:  {sha256_check_verifyer.data}")
            return sha256_verifyer.verify(sha256_check_verifyer.data)

        def verify_sig(filename: str, pemfile: str):
            """Verify if the .zip file is signed correctly"""
            print()
            print(f"⚠  Verifying {filename} with {filename}.sig and {pemfile}")
            sig_check_verifyer = SigCheckVerifyer(filename=f"{filename}.sig")
            pem_check_verifyer = PemCheckVerifyer(filename=pemfile)
            sig_check_verifyer.load()
            pem_check_verifyer.load()
            sig_verifyer = SigVerifyer(
                filename=filename,
                signature=sig_check_verifyer.data,
                pubkey=pem_check_verifyer.data,
            )
            sig_verifyer.load()
            return sig_verifyer.verify()

        def download_and_verify():
            """ "Check files, download if needed, verify integrity and authenticity"""
            FIRMWARE_NAME = f"{args.destdir}/krux-{args.firmware}.zip"
            print()
            print(f"🔍 Verifying {FIRMWARE_NAME}")
            if not os.path.exists(FIRMWARE_NAME):
                zipd = download_zip()
            else:
                answer = input(
                    f"⚠️i Do you want to download {FIRMWARE_NAME} again? [y/n]"
                )
                if answer == "y":
                    zipd = download_zip()
                else:
                    zipd = f"{args.destdir}/krux-{args.firmware}.zip"

            print()
            print(f"🔍 Verifying {FIRMWARE_NAME}.sha256.txt")
            if not os.path.exists(f"{FIRMWARE_NAME}.sha256.txt"):
                download_zip_sha256sum()
            else:
                answer = input(
                    f"⚠️  Do you want to download {FIRMWARE_NAME}.sha256.txt again? [y/n]"
                )
                if answer == "y":
                    download_zip_sha256sum()

            print()
            print(f"🔍 Verifying {FIRMWARE_NAME}.sig")
            if not os.path.exists(f"{FIRMWARE_NAME}.sig"):
                download_zip_sig()
            else:
                answer = input(
                    f"⚠️  Do you want to download {FIRMWARE_NAME}.sig again? [y/n]"
                )
                if answer == "y":
                    download_zip_sig()

            print()
            print(f"🔍 Verifying {args.destdir}/selfcustody.pem")
            if not os.path.exists(f"{args.destdir}/selfcustody.pem"):
                pemfile = download_pem()
            else:
                answer = input(
                    f"⚠️  Do you want to download {args.destdir}/selfcustody.pem again? [y/n]"
                )
                if answer == "y":
                    pemfile = download_pem()
                else:
                    pemfile = f"{args.destdir}/selfcustody.pem"

            if not verify_sha256sum(zipd):
                raise RuntimeError("Invalid sha256sum")
            print("✅ Sha256sum Verified Sucessfully")

            if not verify_sig(zipd, pemfile):
                raise RuntimeError("Invalid signature")
            print("✅ Signature Verified Successfully")

            return zipd

        def download_kboot_beta():
            """Download odudex's beta kboot.kfpkg and prints message"""
            print(f"⚡ Downloading firmware to {args.destdir}/kboot.kfpkg")
            beta = BetaDownloader(
                device=args.device,
                binary_type="kboot.kfpkg",
                destdir=args.destdir,
            )
            beta.download()
            print()

        def download_bin_beta():
            """Download odudex's beta firmware.bin and prints message"""
            print(f"⚡ Downloading firmware to {args.destdir}/firmware.bin")
            beta = BetaDownloader(
                device=args.device,
                binary_type="firmware.bin",
                destdir=args.destdir,
            )
            beta.download()
            print()

        if re.findall(r"odudex/krux_binaries", args.firmware):
            if args.flash:
                KBOOT_NAME = f"{args.destdir}/kboot.kfpkg"
                print()
                print(f"🔍 Verifying {KBOOT_NAME}")
                if not os.path.exists(KBOOT_NAME):
                    download_kboot_beta()
                else:
                    answer = input(
                        " ".join(
                            [
                                f"⚠️  Do you want to download {KBOOT_NAME} for",
                                f"'{args.device}' again? [y/n]",
                            ]
                        )
                    )
                    if answer == "y":
                        download_kboot_beta()

                print()
                print(f"✏️/ Flashing firmware from {KBOOT_NAME}")
                input(
                    " ".join(
                        [
                            f"✋ Please make sure to CONNECT YOUR DEVICE ('{args.device}')",
                            "to the USB port, then press and press ENTER",
                        ]
                    )
                )

                flasher = Flasher(firmware=KBOOT_NAME)
                flasher.flash(device=args.device)
            else:
                FIRMWARE_NAME = f"{args.destdir}/firmware.bin"
                print()
                print(f"🔍 Verifying {FIRMWARE_NAME}")
                if not os.path.exists(FIRMWARE_NAME):
                    download_bin_beta()

                else:
                    answer = input(
                        " ".join(
                            [
                                f"⚠️  Do you want to download {FIRMWARE_NAME} for",
                                f"'{args.device}' again? [y/n]",
                            ]
                        )
                    )
                    if answer == "y":
                        download_bin_beta()

                print(
                    "\n".join(
                        [
                            f"Copy {FIRMWARE_NAME} for '{args.device}' to your SDCard",
                            "then insert the SDCard on the device and turn it on ",
                            "to upgrade the firmware.",
                        ]
                    )
                )

        elif re.findall(r"v2\d\.\d+\.\d+", args.firmware):
            if args.flash:
                ZIPFILE = download_and_verify()

                print()
                print(f"📤 Unzipping {ZIPFILE} for {args.device}")
                unzip = KbootUnzip(
                    filename=ZIPFILE, device=args.device, output=args.destdir
                )
                unzip.load()

                KBOOT_NAME = "/".join(
                    [
                        args.destdir,
                        f"krux-{args.firmware}",
                        f"/maixpy_{args.device}",
                        "kboot.kfpkg",
                    ]
                )

                print()
                print(f"✏️  Flashing {args.firmware} for {args.device}")
                input(
                    " ".join(
                        [
                            f"✋ Please make sure to CONNECT YOUR DEVICE ('{args.device}')",
                            "to the USB port, then press and press ENTER",
                        ]
                    )
                )
                flasher = Flasher(firmware=KBOOT_NAME)
                flasher.flash(device=args.device)

            else:
                ZIPFILE = download_and_verify()

                print()
                print(f"📤 Unzipping {ZIPFILE} for {args.device}")
                unzip = FirmwareUnzip(
                    filename=ZIPFILE, device=args.device, output=args.destdir
                )
                unzip.load()

                FIRMWARE_NAME = "/".join(
                    [
                        args.destdir,
                        f"krux-{args.firmware}",
                        f"/maixpy_{args.device}",
                        "firmware.bin",
                    ]
                )
                print()

                print(
                    "\n".join(
                        [
                            f"Copy {FIRMWARE_NAME} and {FIRMWARE_NAME}.sig for '{args.device}' to your SDCard",
                            "then insert the SDCard on the device and turn it on ",
                            "to upgrade the firmware.",
                        ]
                    )
                )

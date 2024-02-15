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

regcli = r"^(.*krux-installer)(\.py)?(\s--\s)(.*)$"
if not re.findall(regcli, " ".join(sys.argv)):
    print("Reserved to run kivy app")
    
if re.findall(regcli, " ".join(sys.argv)):

    import os
    import tempfile
    from argparse import ArgumentParser
    from src.utils.constants import get_name, get_version, get_description
    from src.utils.selector import Selector, VALID_DEVICES
    from src.utils.downloader import ZipDownloader, Sha256Downloader, SigDownloader, PemDownloader, BetaDownloader
    from src.utils.verifyer import Sha256Verifyer, Sha256CheckVerifyer, SigVerifyer, SigCheckVerifyer, PemCheckVerifyer
    from src.utils.unzip import KbootUnzip, FirmwareUnzip
    from src.utils.flasher import Flasher

    parser = ArgumentParser(
        prog=get_name(),
        description=get_description()
    )

    if sys.platform in ('linux', 'darwin', 'freebsd'):
        parser.add_argument("-v", "--version", help="Show version", action="store_true")
        parser.add_argument("-a", "--available-firmwares", help="Show available versions (require internet connection)", action="store_true")
        parser.add_argument("-A", "--available-devices", help="Show available devices", action="store_true")
        parser.add_argument("-d", "--firmware-device", help="Select a device to be flashed")
        parser.add_argument("-f", "--firmware-version", help="Select a firmware version to be flashed")
        parser.add_argument("-D", "--destdir", help="Directory where assets will be stored (default: OS tmpdir)", default=tempfile.gettempdir())
        parser.add_argument("-F", "--flash", help="If set, download the kboot.kfpkg firmware and flash. Otherwise, download firmware.bin and store in destdir", action="store_true")
    elif sys.platform in ('win32'):
        parser.add_argument("/v", "/version", help="Show version", action="store_true")
        parser.add_argument("/a", "/available-firmwares", help="Show available versions (require internet connection)", action="store_true")
        parser.add_argument("/A", "/available-devices", help="Show available devices", action="store_true")
        parser.add_argument("/d", "/firmware-device", help="Select a device to be flashed")
        parser.add_argument("/f", "/firmware-version", help="Select a firmware version to be flashed")
        parser.add_argument("/D", "/destdir", help="Directory where assets will be stored")
        parser.add_argument("/F", "/flash", help="If set, download the kboot.kfpkg firmware and flash. Otherwise, download firmware.bin and store in destdir ", action="store_true")
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
        for device in VALID_DEVICES:
            print(f"* {device}")
 
    elif args.firmware_device and not args.firmware_version:
        raise RuntimeError(f"Firmware version {args.firmware_version} should be paired with {args.firmware_device}")
    
    elif args.firmware_device and args.firmware_version:

        def download_zip():
            print()
            print(f"⚡ Downloading {args.destdir}/krux-{args.firmware_version}.zip release")
            zip = ZipDownloader(version=args.firmware_version, destdir=args.destdir)
            return zip.download()

        def download_zip_sha256sum():
            print()
            print(f"⚡ Downloading {args.destdir}/krux-{args.firmware_version}.zip.sha256.txt")
            sha256 = Sha256Downloader(version=args.firmware_version, destdir=args.destdir)
            return sha256.download()
        
        def download_zip_sig():
            print()
            print(f"⚡ Downloading {args.destdir}/krux-{args.firmware_version}.zip.sig")
            sig = SigDownloader(version=args.firmware_version, destdir=args.destdir)
            return sig.download()

        def download_pem():
            print()
            print(f"⚡ Downloading {args.destdir}/selfcustody.pem")
            pem = PemDownloader(destdir=args.destdir)
            return pem.download()

        def verify_sha256sum(filename: str):
            print()
            print(f"⚠  Verifying {filename}.zip with {filename}.sha256.txt")
            sha256CheckVerifyer = Sha256CheckVerifyer(filename=f"{filename}.sha256.txt")
            sha256Verifyer = Sha256Verifyer(filename=filename)
            sha256CheckVerifyer.load()
            sha256Verifyer.load()
            print(f"sha256sum: {sha256Verifyer.data}")
            print(f"expected:  {sha256CheckVerifyer.data}")
            return sha256Verifyer.verify(sha256CheckVerifyer.data)

        def verify_sig(filename: str, pemfile: str):
            print()
            print(f"⚠  Verifying {filename} with {filename}.sig and {pemfile}")
            sigCheckVerifyer = SigCheckVerifyer(filename=f"{filename}.sig")
            pemCheckVerifyer = PemCheckVerifyer(filename=pemfile)
            sigCheckVerifyer.load()
            pemCheckVerifyer.load()
            sigVerifyer = SigVerifyer(filename=filename, signature=sigCheckVerifyer.data, pubkey=pemCheckVerifyer.data)
            sigVerifyer.load()
            return sigVerifyer.verify()
            
        def download_and_verify():
            print()
            print(f"🔍 Verifying {args.destdir}/krux-{args.firmware_version}.zip")
            if not os.path.exists(f"{args.destdir}/krux-{args.firmware_version}.zip"):
                zipfile = download_zip()
            else:
                answer = input(f"⚠  Do you want to download {args.destdir}/krux-{args.firmware_version}.zip again? [y/n]")
                if answer == "y":
                    zipfile = download_zip()
                else:
                    zipfile = f"{args.destdir}/krux-{args.firmware_version}.zip"
                    
            print()
            print(f"🔍 Verifying {args.destdir}/krux-{args.firmware_version}.zip.sha256.txt")
            if not os.path.exists(f"{zipfile}.sha256.txt"):
                download_zip_sha256sum()
            else:
                answer = input(f"⚠  Do you want to download {zipfile}.sha256.txt again? [y/n]")
                if answer == "y":
                    download_zip_sha256sum()

            print()
            print(f"🔍 Verifying {args.destdir}/krux-{args.firmware_version}.sig")
            if not os.path.exists(f"{zipfile}.sig"):
                download_zip_sig()
            else:
                answer = input(f"⚠ Do you want to download {zipfile}.sig again? [y/n]")
                if answer == "y":
                    download_zip_sig()
            
            print()
            print(f"🔍 Verifying {args.destdir}/selfcustody.pem")
            if not os.path.exists(f"{args.destdir}/selfcustody.pem"):
                pemfile = download_pem()
            else:
                answer = input(f"⚠ Do you want to download {args.destdir}/selfcustody.pem again? [y/n]")
                if answer == "y":
                    pemfile = download_pem()
                else:
                    pemfile = f"{args.destdir}/selfcustody.pem"
                
            if not verify_sha256sum(zipfile):
                raise RuntimeError("Invalid sha256sum")
            else:
                print("✅ Sha256sum Verified Sucessfully")

            if not verify_sig(zipfile, pemfile):
                raise RuntimeError("Invalid signature")
            else:
                print("✅ Signature Verified Successfully")

            return zipfile
            
        if re.findall(r"odudex/krux_binaries", args.firmware_version):
            if args.flash:
                print()
                print(f"⚡ Downloading firmware to {args.destdir}/maixpy_{args.firmware_device}/kboot.kfpkg")
                beta = BetaDownloader(device=args.firmware_device, binary_type="kboot", destdir=args.destdir)
                beta.load()
                print()                
                print(f"✎ Flashing firmware from {args.destdir}/maixpy_{args.firmware_device}/kboot.kfpkg")
                flasher = Flasher(firmware=f"{beta.destdir}/maixpy_{args.firmware_device}/kboot.kfpkg")
                flasher.flash()
            else:                
                print()
                print(f"⚡ Downloading firmware to {args.destdir}/maixpy_{args.firmware_device}/firmware.bin(.sig)")
                beta = BetaDownloader(device=args.firmware_device, binary_type="firmware", destdir=args.destdir)
                beta.load()
                print()
    
    
        elif re.findall(r"v2\d\.\d+\.\d+", args.firmware_version):
            if args.flash:
                zipfile = download_and_verify()

                print()
                print(f"📤 Unzipping {zipfile} for {args.firmware_device}")
                unzip = KbootUnzip(filename=zipfile, device=args.firmware_device, output=args.destdir)
                unzip.load()

                print()
                print(f"✎ Flashing {args.firmware_version} for {args.firmware_device}")
                flasher = Flasher(firmware=f"{args.destdir}/krux-{args.firmware_version}/maixpy_{args.firmware_device}/kboot.kfpkg")
                flasher.flash()
            
            else:
                zipfile = download_and_verify()
                
                print()
                print(f"📤 Unzipping {zipfile} for {args.firmware_device}")
                unzip = FirmwareUnzip(filename=zipfile, device=args.firmware_device, output=args.destdir)
                unzip.load()
                print()
                
                print(f"Copy {args.destdir}/krux-{args.firmware_version}/maixpy_{args.firmware_device}/firmware.bin to your SDCard")
                print(f"Copy {args.destdir}/krux-{args.firmware_version}/maixpy_{args.firmware_device}/firmware.bin.sig to your SDCard")
            
            
                
            
            
    

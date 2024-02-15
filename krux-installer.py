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
from argparse import ArgumentParser
from src.utils.constants import get_name, get_version, get_description
from src.utils.selector import Selector, VALID_DEVICES
from src.utils.downloader import ZipDownloader, Sha256Downloader, SigDownloader, PemDownloader, BetaDownloader
from src.utils.verifyer import Sha256Verifyer, Sha256CheckVerifyer, SigVerifyer, SigCheckVerifyer, PemCheckVerifyer
from src.utils.unzip import KbootUnzip
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
    parser.add_argument("-D", "--destdir", help="Directory where assets will be stored")
    parser.add_argument("-F", "--flash", help="If set, download the kboot.kfpkg firmware and flash. Otherwise, download firmware.bin and store in destdir", action="store_true")
    parser.add_argument("-g", "--gui", help="Run kivy app")
elif sys.platform in ('win32'):
    parser.add_argument("/v", "/version", help="Show version", action="store_true")
    parser.add_argument("/a", "/available-firmwares", help="Show available versions (require internet connection)", action="store_true")
    parser.add_argument("/A", "/available-devices", help="Show available devices", action="store_true")
    parser.add_argument("/d", "/firmware-device", help="Select a device to be flashed")
    parser.add_argument("/f", "/firmware-version", help="Select a firmware version to be flashed")
    parser.add_argument("/D", "/destdir", help="Directory where assets will be stored")
    parser.add_argument("/F", "/flash", help="If set, flash the firmware. Else only download data", action="store_true")
    parser.add_argument("/g", "/gui", help="Run kivy app")
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

    if re.findall(r"odudex/krux_binaries", args.firmware_version):
        if args.flash and args.destdir:
            beta = BetaDownloader(device=args.firmware_device, binary_type="kboot", destdir=args.destdir)
            beta.load()
            flasher = Flasher(firmware=f"{beta.destdir}/maixpy_{args.firmware_device}/kboot.kfpkg")
            flasher.flash()
            
        elif args.flash and not args.destdir:            
            beta = BetaDownloader(device=args.firmware_device, binary_type="kboot")
            beta.load()
            flasher = Flasher(firmware=f"{beta.destdir}/maixpy_{args.firmware_device}/kboot.kfpkg")
            flasher.flash()
            
        elif not args.flash and args.destdir:
            beta = BetaDownloader(device=args.firmware_device, binary_type="firmware", destdir=args.destdir)
            beta.load()
    
        elif not args.flash and not args.destdir:
            beta = BetaDownloader(device=args.firmware_device, binary_type="firmware")
            beta.load()
    
    elif re.findall(r"v2\d\.\d+\.\d+", args.firmware_version):
        
        if args.flash and args.destdir:
            print()
            print(f"Downloading {args.destdir}/krux-{args.firmware_version}.zip release")
            zip = ZipDownloader(version=args.firmware_version, destdir=args.destdir)
            zipfile = zip.download()
            print()
            
            print(f"Downloading {zipfile}.sha256.txt")
            sha256 = Sha256Downloader(version=args.firmware_version, destdir=args.destdir)
            sha256file = sha256.download()
            print()
            
            print(f"Downloading {zipfile}.sig")
            sig = SigDownloader(version=args.firmware_version, destdir=args.destdir)
            sigfile = sig.download()
            print()

            print(f"Downloading {args.destdir}/selfcustody.pem")
            pem = PemDownloader(destdir=args.destdir)
            pemfile = pem.download()
            print()

            print()
            print(f"Verifying {zipfile} with {sha256file}")
            sha256CheckVerifyer = Sha256CheckVerifyer(filename=sha256file)
            sha256Verifyer = Sha256Verifyer(filename=zipfile)
            sha256CheckVerifyer.load()
            sha256Verifyer.load()

            print(f"sha256sum: {sha256Verifyer.data}")
            print(f"expected:  {sha256CheckVerifyer.data}")
            result = sha256Verifyer.verify(sha256CheckVerifyer.data)
            
            if not result:
                raise RuntimeError(f"Invalid sha256sum")
            else:
                print("Sha256sum Verified Sucessfully")

            print()
            print(f"Verifying {zipfile} with {sigfile}")
            sigCheckVerifyer = SigCheckVerifyer(filename=sigfile)
            pemCheckVerifyer = PemCheckVerifyer(filename=pemfile)
            sigCheckVerifyer.load()
            pemCheckVerifyer.load()
            sigVerifyer = SigVerifyer(filename=zipfile, signature=sigCheckVerifyer.data, pubkey=pemCheckVerifyer.data)
            sigVerifyer.load()
            result = sigVerifyer.verify()
            
            if not result:
                raise RuntimeError(f"Invalid signature")
            else:
                print("Signature Verified Successfully")

            print()
            print(f"Unzipping {zipfile} for {args.firmware_device}")
            unzip = KbootUnzip(filename=zipfile, device=args.firmware_device, output=args.destdir)
            unzip.load()
            print()

            print(f"Flashing {args.firmware_version} for {args.firmware_device}")
            flasher = Flasher(firmware=f"{args.destdir}/krux-{args.firmware_version}/maixpy_{args.firmware_device}/kboot.kfpkg")
            flasher.flash()

            
            
                
            
            
    

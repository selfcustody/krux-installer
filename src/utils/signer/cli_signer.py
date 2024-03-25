# The MIT License (MIT)

# Copyright (c) 2021-2023 Krux contributors

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
cli_signer.py
"""
import re
import cv2
from qrcode import QRCode
from .trigger_signer import TriggerSigner


class CliSigner(TriggerSigner):
    """Signer for Command Line Interface"""

    def __init__(self, filename: str):
        super().__init__(filename=filename)

    def print_scan_hash_message(self):
        """Print some warnings to start the process of signing"""
        print("=====================================================")
        print("To sign this file with Krux: ")
        print(" (a) load a 12/24 words key with or without password;")
        print(" (b) use the Sign->Message feature;")
        print(" (c) and scan this QR code below.")
        print("=====================================================")
        print("")

    def print_scan_signature_message(self):
        """Print some warning to scan signature"""
        print("")
        print("=====================================================")
        input("Press enter to scan signature")
        print("=====================================================")
        print("")

    def print_scan_pubkey_message(self):
        """Print some warning to scan public key certificate"""
        print("")
        print("=====================================================")
        input("Press enter to scan public key")
        print("=====================================================")
        print("")

    def scan(self):
        """
        Open a scan window and uses cv2 to detect and
        decode a QRCode, returning its data
        """
        vid = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()
        qr_data = None

        while True:
            # Capture the video frame by frame
            # use some dummy vars (__+[a-zA-Z0-9]*?$)
            # to avoid the W0612 'Unused variable' pylint message
            _ret, frame = vid.read()

            # delattrtect qrcode
            qr_data, _bbox, _straight_qrcode = detector.detectAndDecode(frame)

            # Verify null data
            if len(qr_data) > 0:
                break

            # Display the resulting frame
            cv2.imshow("frame", frame)

            # the 'q' button is set as the
            # quitting button you may use any
            # desired button of your choice
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        vid.release()
        cv2.destroyAllWindows()

        return qr_data

    def print_hash(self):
        """Print sha256sum in qrcode format"""
        if self.filehash is None:
            raise ValueError(f"Empty hash: {self.filehash}")

        if re.findall(r"^[a-f0-9]{64}$", self.filehash):
            qrcode = QRCode()
            qrcode.add_data(self.filehash)
            qrcode.print_ascii(invert=True)

        else:
            raise ValueError(f"Invalid hash: '{self.filehash}'")

    def make_signature(self):
        """Create a signature data"""
        self.signature = self.scan()

    def make_pubkey(self):
        """Create a pubkey certificate"""
        self.pubkey = self.scan()

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
sha256_verifyer.py
"""

import typing
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization, hashes, asymmetric
from .check_verifyer import CheckVerifyer


class SigVerifyer(CheckVerifyer):
    """Verify file signature agains .sig and .pem data"""

    def __init__(self, filename: str, signature: str, pubkey: str, regexp: typing.re):
        super().__init__(filename=filename, read_mode="rb", regexp=regexp)
        self.certificate = serialization.load_pem_public_key(pubkey)
        self.signature = signature

    def verify(self) -> bool:
        """Apply signature verification against a signature data and public key data"""
        try:
            algorithm = asymmetric.ec.ECDSA(hashes.SHA256())
            self.certificate.verify(self.signature, self.data, algorithm)
            return True
        except InvalidSignature:
            return False

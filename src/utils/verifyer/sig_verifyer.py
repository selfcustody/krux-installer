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
from ssl import SSLWantReadError, SSLSyscallError, SSLError
from OpenSSL.crypto import (
    X509,
    load_publickey,
    FILETYPE_PEM,
    verify as openssl_verify
)
from .check_verifyer import CheckVerifyer


class SigVerifyer(CheckVerifyer):
    """Verify file signature agains .sig and .pem data"""

    def __init__(self, filename: str, signature: str, pubkey: str):
        super().__init__(filename=filename, read_mode="rb", regexp=r".*\.zip")
        self.x509 = X509()
        _pubkey = load_publickey(FILETYPE_PEM, pubkey)
        self.x509.set_pubkey(_pubkey)
        self.signature = signature

    @property
    def x509(self) -> X509:
        """Getter for x509 object"""
        self.debug(f"x509::getter={self._x509}")
        return self._x509

    @x509.setter
    def x509(self, value: X509):
        self.debug(f"x509::setter={value}")
        self._x509 = value

    @property
    def signature(self) -> typing.SupportsBytes:
        """Getter for signature bytes"""
        self.debug(f"signature::getter={self._signature}")
        return self._signature

    @signature.setter
    def signature(self, value: typing.SupportsBytes):
        """Set the public key on X509 object"""
        self.debug(f"signature::setter={value}")
        self._signature = value

    def verify(self):
        """Apply signature verification against a signature data and public key data"""
        try:
            openssl_verify(self.x509, self.signature, self.data, "sha256")
            return "Signature Verified Successfully"
        except SSLError as exc_info:
            raise ValueError(
                f"SSLError {exc_info.strerror}: {exc_info.reason}"
            ) from exc_info
        except SSLSyscallError as exc_info:
            raise ValueError(
                f"SSLSyscallError {exc_info.strerror}: {exc_info.reason}"
            ) from exc_info
        except SSLWantReadError as exc_info:
            raise ValueError(
                f"SSLWantReadError {exc_info.strerror}: {exc_info.reason}"
            ) from exc_info

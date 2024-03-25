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
base_signer.py
"""
import os
import re
import base64
import typing
from ..trigger import Trigger


ASN1_STRUCTURE_FOR_PUBKEY = "3036301006072A8648CE3D020106052B8104000A032200"
"""
ASN.1 STRUCTURE FOR PUBKEY (uncompressed and compressed):
   30  <-- declares the start of an ASN.1 sequence
   56  <-- length of following sequence (dez 86)
   30  <-- length declaration is following
   10  <-- length of integer in bytes (dez 16)
   06  <-- declares the start of an "octet string"
   07  <-- length of integer in bytes (dez 7)
   2A 86 48 CE 3D 02 01 <-- Object Identifier: 1.2.840.10045.2.1
                            = ecPublicKey, ANSI X9.62 public key type
   06  <-- declares the start of an "octet string"
   05  <-- length of integer in bytes (dez 5)
   2B 81 04 00 0A <-- Object Identifier: 1.3.132.0.10
                      = secp256k1, SECG (Certicom) named eliptic curve
   03  <-- declares the start of an "octet string"
   42  <-- length of bit string to follow (66 bytes)
   00  <-- Start pubkey?? 
"""


class BaseSigner(Trigger):
    """
    BaseSigner
    """

    def __init__(self, filename: str):
        super().__init__()
        self.filename = filename

    @property
    def filename(self) -> str:
        """Getter for filename"""
        self.debug(f"filename::getter={self._filename}")
        return self._filename

    @filename.setter
    def filename(self, value: str):
        """Setter for filename"""
        if os.path.exists(value):
            self.debug(f"filename::setter={value}")
            self._filename = value
        else:
            raise ValueError(f"{value} do not exists")

    @property
    def filehash(self) -> str:
        """Getter for filehash"""
        self.debug(f"filehash::getter={self._filehash}")
        return self._filehash

    @filehash.setter
    def filehash(self, value: str):
        """Setter for filehash"""
        if re.findall(r"[a-fA-F0-9]{64}", value):
            self.debug(f"filehash::setter={value}")
            self._filehash = value
        else:
            raise ValueError(f"Invalid hash: {value}")

    @property
    def signature(self) -> typing.SupportsBytes:
        """Getter for signature in byte format"""
        self.debug(f"signature::getter={self._signature}")
        return self._signature

    @signature.setter
    def signature(self, value: str):
        """Setter for signature giving a well formated string"""
        if re.findall(
            r"^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$", value
        ):
            self.debug(f"signature::setter={value}")
            self._signature = base64.b64decode(value.encode())
        else:
            raise ValueError(f"Invalid signature: {value}")

    @property
    def pubkey(self) -> str:
        """Getter for public key certificate"""
        self.debug(f"pubkey::getter={self._pubkey}")
        return self._pubkey

    @pubkey.setter
    def pubkey(self, value: typing.SupportsBytes):
        """Setter for public key certificate"""
        if re.findall("[a-f0-9]{64}", value):
            self.debug(f"pubkey::setter={value}")
            pubkey_data = f"{ASN1_STRUCTURE_FOR_PUBKEY}{value}"

            # Convert pubkey data to bytes
            pubkey_data_bytes = bytes.fromhex(pubkey_data)

            # Encoding bytes to base64 format
            pubkey_data_b64 = base64.b64encode(pubkey_data_bytes)

            # Decode base64 to utf8
            self._pubkey = pubkey_data_b64.decode("utf8")
        else:
            raise ValueError(f"Invalid pubkey: {value}")

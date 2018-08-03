# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pyrogram.api.core import *


class ReqDHParams(Object):
    """Attributes:
        ID: ``0xd712e4be``

    Args:
        nonce: ``int`` ``128-bit``
        server_nonce: ``int`` ``128-bit``
        p: ``bytes``
        q: ``bytes``
        public_key_fingerprint: ``int`` ``64-bit``
        encrypted_data: ``bytes``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`ServerDHParamsFail <pyrogram.api.types.ServerDHParamsFail>` or :obj:`ServerDHParamsOk <pyrogram.api.types.ServerDHParamsOk>`
    """

    ID = 0xd712e4be

    def __init__(self, nonce: int, server_nonce: int, p: bytes, q: bytes, public_key_fingerprint: int, encrypted_data: bytes):
        self.nonce = nonce  # int128
        self.server_nonce = server_nonce  # int128
        self.p = p  # bytes
        self.q = q  # bytes
        self.public_key_fingerprint = public_key_fingerprint  # long
        self.encrypted_data = encrypted_data  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "ReqDHParams":
        # No flags
        
        nonce = Int128.read(b)
        
        server_nonce = Int128.read(b)
        
        p = Bytes.read(b)
        
        q = Bytes.read(b)
        
        public_key_fingerprint = Long.read(b)
        
        encrypted_data = Bytes.read(b)
        
        return ReqDHParams(nonce, server_nonce, p, q, public_key_fingerprint, encrypted_data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int128(self.nonce))
        
        b.write(Int128(self.server_nonce))
        
        b.write(Bytes(self.p))
        
        b.write(Bytes(self.q))
        
        b.write(Long(self.public_key_fingerprint))
        
        b.write(Bytes(self.encrypted_data))
        
        return b.getvalue()

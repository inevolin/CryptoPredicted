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


class SetClientDHParams(Object):
    """Attributes:
        ID: ``0xf5045f1f``

    Args:
        nonce: ``int`` ``128-bit``
        server_nonce: ``int`` ``128-bit``
        encrypted_data: ``bytes``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`DhGenOk <pyrogram.api.types.DhGenOk>`, :obj:`DhGenRetry <pyrogram.api.types.DhGenRetry>` or :obj:`DhGenFail <pyrogram.api.types.DhGenFail>`
    """

    ID = 0xf5045f1f

    def __init__(self, nonce: int, server_nonce: int, encrypted_data: bytes):
        self.nonce = nonce  # int128
        self.server_nonce = server_nonce  # int128
        self.encrypted_data = encrypted_data  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SetClientDHParams":
        # No flags
        
        nonce = Int128.read(b)
        
        server_nonce = Int128.read(b)
        
        encrypted_data = Bytes.read(b)
        
        return SetClientDHParams(nonce, server_nonce, encrypted_data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int128(self.nonce))
        
        b.write(Int128(self.server_nonce))
        
        b.write(Bytes(self.encrypted_data))
        
        return b.getvalue()

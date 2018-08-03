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


class DhGenOk(Object):
    """Attributes:
        ID: ``0x3bcbf734``

    Args:
        nonce: ``int`` ``128-bit``
        server_nonce: ``int`` ``128-bit``
        new_nonce_hash1: ``int`` ``128-bit``

    See Also:
        This object can be returned by :obj:`SetClientDHParams <pyrogram.api.functions.SetClientDHParams>`.
    """

    ID = 0x3bcbf734

    def __init__(self, nonce: int, server_nonce: int, new_nonce_hash1: int):
        self.nonce = nonce  # int128
        self.server_nonce = server_nonce  # int128
        self.new_nonce_hash1 = new_nonce_hash1  # int128

    @staticmethod
    def read(b: BytesIO, *args) -> "DhGenOk":
        # No flags
        
        nonce = Int128.read(b)
        
        server_nonce = Int128.read(b)
        
        new_nonce_hash1 = Int128.read(b)
        
        return DhGenOk(nonce, server_nonce, new_nonce_hash1)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int128(self.nonce))
        
        b.write(Int128(self.server_nonce))
        
        b.write(Int128(self.new_nonce_hash1))
        
        return b.getvalue()

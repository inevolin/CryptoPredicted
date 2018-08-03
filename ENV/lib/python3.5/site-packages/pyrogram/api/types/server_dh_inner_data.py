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


class ServerDHInnerData(Object):
    """Attributes:
        ID: ``0xb5890dba``

    Args:
        nonce: ``int`` ``128-bit``
        server_nonce: ``int`` ``128-bit``
        g: ``int`` ``32-bit``
        dh_prime: ``bytes``
        g_a: ``bytes``
        server_time: ``int`` ``32-bit``
    """

    ID = 0xb5890dba

    def __init__(self, nonce: int, server_nonce: int, g: int, dh_prime: bytes, g_a: bytes, server_time: int):
        self.nonce = nonce  # int128
        self.server_nonce = server_nonce  # int128
        self.g = g  # int
        self.dh_prime = dh_prime  # bytes
        self.g_a = g_a  # bytes
        self.server_time = server_time  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ServerDHInnerData":
        # No flags
        
        nonce = Int128.read(b)
        
        server_nonce = Int128.read(b)
        
        g = Int.read(b)
        
        dh_prime = Bytes.read(b)
        
        g_a = Bytes.read(b)
        
        server_time = Int.read(b)
        
        return ServerDHInnerData(nonce, server_nonce, g, dh_prime, g_a, server_time)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int128(self.nonce))
        
        b.write(Int128(self.server_nonce))
        
        b.write(Int(self.g))
        
        b.write(Bytes(self.dh_prime))
        
        b.write(Bytes(self.g_a))
        
        b.write(Int(self.server_time))
        
        return b.getvalue()

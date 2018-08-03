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


class DhConfig(Object):
    """Attributes:
        ID: ``0x2c221edd``

    Args:
        g: ``int`` ``32-bit``
        p: ``bytes``
        version: ``int`` ``32-bit``
        random: ``bytes``

    See Also:
        This object can be returned by :obj:`messages.GetDhConfig <pyrogram.api.functions.messages.GetDhConfig>`.
    """

    ID = 0x2c221edd

    def __init__(self, g: int, p: bytes, version: int, random: bytes):
        self.g = g  # int
        self.p = p  # bytes
        self.version = version  # int
        self.random = random  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "DhConfig":
        # No flags
        
        g = Int.read(b)
        
        p = Bytes.read(b)
        
        version = Int.read(b)
        
        random = Bytes.read(b)
        
        return DhConfig(g, p, version, random)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.g))
        
        b.write(Bytes(self.p))
        
        b.write(Int(self.version))
        
        b.write(Bytes(self.random))
        
        return b.getvalue()

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


class PhotoCachedSize(Object):
    """Attributes:
        ID: ``0xe9a734fa``

    Args:
        type: ``str``
        location: Either :obj:`FileLocationUnavailable <pyrogram.api.types.FileLocationUnavailable>` or :obj:`FileLocation <pyrogram.api.types.FileLocation>`
        w: ``int`` ``32-bit``
        h: ``int`` ``32-bit``
        bytes: ``bytes``
    """

    ID = 0xe9a734fa

    def __init__(self, type: str, location, w: int, h: int, bytes: bytes):
        self.type = type  # string
        self.location = location  # FileLocation
        self.w = w  # int
        self.h = h  # int
        self.bytes = bytes  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "PhotoCachedSize":
        # No flags
        
        type = String.read(b)
        
        location = Object.read(b)
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        bytes = Bytes.read(b)
        
        return PhotoCachedSize(type, location, w, h, bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.type))
        
        b.write(self.location.write())
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        b.write(Bytes(self.bytes))
        
        return b.getvalue()

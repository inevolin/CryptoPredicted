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


class Photo(Object):
    """Attributes:
        ID: ``0x9288dd29``

    Args:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        date: ``int`` ``32-bit``
        sizes: List of either :obj:`PhotoSizeEmpty <pyrogram.api.types.PhotoSizeEmpty>`, :obj:`PhotoSize <pyrogram.api.types.PhotoSize>` or :obj:`PhotoCachedSize <pyrogram.api.types.PhotoCachedSize>`
        has_stickers (optional): ``bool``
    """

    ID = 0x9288dd29

    def __init__(self, id: int, access_hash: int, date: int, sizes: list, has_stickers: bool = None):
        self.has_stickers = has_stickers  # flags.0?true
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.date = date  # int
        self.sizes = sizes  # Vector<PhotoSize>

    @staticmethod
    def read(b: BytesIO, *args) -> "Photo":
        flags = Int.read(b)
        
        has_stickers = True if flags & (1 << 0) else False
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        date = Int.read(b)
        
        sizes = Object.read(b)
        
        return Photo(id, access_hash, date, sizes, has_stickers)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.has_stickers is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(Int(self.date))
        
        b.write(Vector(self.sizes))
        
        return b.getvalue()

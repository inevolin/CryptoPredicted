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


class WallPaper(Object):
    """Attributes:
        ID: ``0xccb03657``

    Args:
        id: ``int`` ``32-bit``
        title: ``str``
        sizes: List of either :obj:`PhotoSizeEmpty <pyrogram.api.types.PhotoSizeEmpty>`, :obj:`PhotoSize <pyrogram.api.types.PhotoSize>` or :obj:`PhotoCachedSize <pyrogram.api.types.PhotoCachedSize>`
        color: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`account.GetWallPapers <pyrogram.api.functions.account.GetWallPapers>`.
    """

    ID = 0xccb03657

    def __init__(self, id: int, title: str, sizes: list, color: int):
        self.id = id  # int
        self.title = title  # string
        self.sizes = sizes  # Vector<PhotoSize>
        self.color = color  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "WallPaper":
        # No flags
        
        id = Int.read(b)
        
        title = String.read(b)
        
        sizes = Object.read(b)
        
        color = Int.read(b)
        
        return WallPaper(id, title, sizes, color)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(String(self.title))
        
        b.write(Vector(self.sizes))
        
        b.write(Int(self.color))
        
        return b.getvalue()

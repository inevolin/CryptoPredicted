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


class WallPaperSolid(Object):
    """Attributes:
        ID: ``0x63117f24``

    Args:
        id: ``int`` ``32-bit``
        title: ``str``
        bg_color: ``int`` ``32-bit``
        color: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`account.GetWallPapers <pyrogram.api.functions.account.GetWallPapers>`.
    """

    ID = 0x63117f24

    def __init__(self, id: int, title: str, bg_color: int, color: int):
        self.id = id  # int
        self.title = title  # string
        self.bg_color = bg_color  # int
        self.color = color  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "WallPaperSolid":
        # No flags
        
        id = Int.read(b)
        
        title = String.read(b)
        
        bg_color = Int.read(b)
        
        color = Int.read(b)
        
        return WallPaperSolid(id, title, bg_color, color)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(String(self.title))
        
        b.write(Int(self.bg_color))
        
        b.write(Int(self.color))
        
        return b.getvalue()

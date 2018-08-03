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


class FeaturedStickers(Object):
    """Attributes:
        ID: ``0xf89d88e5``

    Args:
        hash: ``int`` ``32-bit``
        sets: List of either :obj:`StickerSetCovered <pyrogram.api.types.StickerSetCovered>` or :obj:`StickerSetMultiCovered <pyrogram.api.types.StickerSetMultiCovered>`
        unread: List of ``int`` ``64-bit``

    See Also:
        This object can be returned by :obj:`messages.GetFeaturedStickers <pyrogram.api.functions.messages.GetFeaturedStickers>`.
    """

    ID = 0xf89d88e5

    def __init__(self, hash: int, sets: list, unread: list):
        self.hash = hash  # int
        self.sets = sets  # Vector<StickerSetCovered>
        self.unread = unread  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args) -> "FeaturedStickers":
        # No flags
        
        hash = Int.read(b)
        
        sets = Object.read(b)
        
        unread = Object.read(b, Long)
        
        return FeaturedStickers(hash, sets, unread)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.sets))
        
        b.write(Vector(self.unread, Long))
        
        return b.getvalue()

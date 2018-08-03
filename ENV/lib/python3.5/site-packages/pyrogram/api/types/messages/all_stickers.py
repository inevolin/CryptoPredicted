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


class AllStickers(Object):
    """Attributes:
        ID: ``0xedfd405f``

    Args:
        hash: ``int`` ``32-bit``
        sets: List of :obj:`StickerSet <pyrogram.api.types.StickerSet>`

    See Also:
        This object can be returned by :obj:`messages.GetAllStickers <pyrogram.api.functions.messages.GetAllStickers>` and :obj:`messages.GetMaskStickers <pyrogram.api.functions.messages.GetMaskStickers>`.
    """

    ID = 0xedfd405f

    def __init__(self, hash: int, sets: list):
        self.hash = hash  # int
        self.sets = sets  # Vector<StickerSet>

    @staticmethod
    def read(b: BytesIO, *args) -> "AllStickers":
        # No flags
        
        hash = Int.read(b)
        
        sets = Object.read(b)
        
        return AllStickers(hash, sets)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.sets))
        
        return b.getvalue()

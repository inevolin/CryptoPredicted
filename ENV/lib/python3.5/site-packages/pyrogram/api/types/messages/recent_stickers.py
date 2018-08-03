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


class RecentStickers(Object):
    """Attributes:
        ID: ``0x22f3afb3``

    Args:
        hash: ``int`` ``32-bit``
        packs: List of :obj:`StickerPack <pyrogram.api.types.StickerPack>`
        stickers: List of either :obj:`DocumentEmpty <pyrogram.api.types.DocumentEmpty>` or :obj:`Document <pyrogram.api.types.Document>`
        dates: List of ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.GetRecentStickers <pyrogram.api.functions.messages.GetRecentStickers>`.
    """

    ID = 0x22f3afb3

    def __init__(self, hash: int, packs: list, stickers: list, dates: list):
        self.hash = hash  # int
        self.packs = packs  # Vector<StickerPack>
        self.stickers = stickers  # Vector<Document>
        self.dates = dates  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args) -> "RecentStickers":
        # No flags
        
        hash = Int.read(b)
        
        packs = Object.read(b)
        
        stickers = Object.read(b)
        
        dates = Object.read(b, Int)
        
        return RecentStickers(hash, packs, stickers, dates)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.packs))
        
        b.write(Vector(self.stickers))
        
        b.write(Vector(self.dates, Int))
        
        return b.getvalue()

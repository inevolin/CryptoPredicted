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


class SearchStickerSets(Object):
    """Attributes:
        ID: ``0xc2b7d08b``

    Args:
        q: ``str``
        hash: ``int`` ``32-bit``
        exclude_featured (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.FoundStickerSetsNotModified <pyrogram.api.types.messages.FoundStickerSetsNotModified>` or :obj:`messages.FoundStickerSets <pyrogram.api.types.messages.FoundStickerSets>`
    """

    ID = 0xc2b7d08b

    def __init__(self, q: str, hash: int, exclude_featured: bool = None):
        self.exclude_featured = exclude_featured  # flags.0?true
        self.q = q  # string
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SearchStickerSets":
        flags = Int.read(b)
        
        exclude_featured = True if flags & (1 << 0) else False
        q = String.read(b)
        
        hash = Int.read(b)
        
        return SearchStickerSets(q, hash, exclude_featured)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.exclude_featured is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.q))
        
        b.write(Int(self.hash))
        
        return b.getvalue()

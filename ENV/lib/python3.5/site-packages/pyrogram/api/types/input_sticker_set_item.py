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


class InputStickerSetItem(Object):
    """Attributes:
        ID: ``0xffa0a496``

    Args:
        document: Either :obj:`InputDocumentEmpty <pyrogram.api.types.InputDocumentEmpty>` or :obj:`InputDocument <pyrogram.api.types.InputDocument>`
        emoji: ``str``
        mask_coords (optional): :obj:`MaskCoords <pyrogram.api.types.MaskCoords>`
    """

    ID = 0xffa0a496

    def __init__(self, document, emoji: str, mask_coords=None):
        self.document = document  # InputDocument
        self.emoji = emoji  # string
        self.mask_coords = mask_coords  # flags.0?MaskCoords

    @staticmethod
    def read(b: BytesIO, *args) -> "InputStickerSetItem":
        flags = Int.read(b)
        
        document = Object.read(b)
        
        emoji = String.read(b)
        
        mask_coords = Object.read(b) if flags & (1 << 0) else None
        
        return InputStickerSetItem(document, emoji, mask_coords)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.mask_coords is not None else 0
        b.write(Int(flags))
        
        b.write(self.document.write())
        
        b.write(String(self.emoji))
        
        if self.mask_coords is not None:
            b.write(self.mask_coords.write())
        
        return b.getvalue()

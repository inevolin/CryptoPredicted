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


class GetStickers(Object):
    """Attributes:
        ID: ``0x043d4f2c``

    Args:
        emoticon: ``str``
        hash: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.StickersNotModified <pyrogram.api.types.messages.StickersNotModified>` or :obj:`messages.Stickers <pyrogram.api.types.messages.Stickers>`
    """

    ID = 0x043d4f2c

    def __init__(self, emoticon: str, hash: int):
        self.emoticon = emoticon  # string
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetStickers":
        # No flags
        
        emoticon = String.read(b)
        
        hash = Int.read(b)
        
        return GetStickers(emoticon, hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.emoticon))
        
        b.write(Int(self.hash))
        
        return b.getvalue()

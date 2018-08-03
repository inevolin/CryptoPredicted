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


class FoundGif(Object):
    """Attributes:
        ID: ``0x162ecc1f``

    Args:
        url: ``str``
        thumb_url: ``str``
        content_url: ``str``
        content_type: ``str``
        w: ``int`` ``32-bit``
        h: ``int`` ``32-bit``
    """

    ID = 0x162ecc1f

    def __init__(self, url: str, thumb_url: str, content_url: str, content_type: str, w: int, h: int):
        self.url = url  # string
        self.thumb_url = thumb_url  # string
        self.content_url = content_url  # string
        self.content_type = content_type  # string
        self.w = w  # int
        self.h = h  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "FoundGif":
        # No flags
        
        url = String.read(b)
        
        thumb_url = String.read(b)
        
        content_url = String.read(b)
        
        content_type = String.read(b)
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        return FoundGif(url, thumb_url, content_url, content_type, w, h)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(String(self.thumb_url))
        
        b.write(String(self.content_url))
        
        b.write(String(self.content_type))
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        return b.getvalue()

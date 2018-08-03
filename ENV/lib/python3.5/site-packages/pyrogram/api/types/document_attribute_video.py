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


class DocumentAttributeVideo(Object):
    """Attributes:
        ID: ``0x0ef02ce6``

    Args:
        duration: ``int`` ``32-bit``
        w: ``int`` ``32-bit``
        h: ``int`` ``32-bit``
        round_message (optional): ``bool``
        supports_streaming (optional): ``bool``
    """

    ID = 0x0ef02ce6

    def __init__(self, duration: int, w: int, h: int, round_message: bool = None, supports_streaming: bool = None):
        self.round_message = round_message  # flags.0?true
        self.supports_streaming = supports_streaming  # flags.1?true
        self.duration = duration  # int
        self.w = w  # int
        self.h = h  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "DocumentAttributeVideo":
        flags = Int.read(b)
        
        round_message = True if flags & (1 << 0) else False
        supports_streaming = True if flags & (1 << 1) else False
        duration = Int.read(b)
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        return DocumentAttributeVideo(duration, w, h, round_message, supports_streaming)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.round_message is not None else 0
        flags |= (1 << 1) if self.supports_streaming is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.duration))
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        return b.getvalue()

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


class DocumentAttributeImageSize(Object):
    """Attributes:
        ID: ``0x6c37c15c``

    Args:
        w: ``int`` ``32-bit``
        h: ``int`` ``32-bit``
    """

    ID = 0x6c37c15c

    def __init__(self, w: int, h: int):
        self.w = w  # int
        self.h = h  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "DocumentAttributeImageSize":
        # No flags
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        return DocumentAttributeImageSize(w, h)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        return b.getvalue()

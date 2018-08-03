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


class ReorderStickerSets(Object):
    """Attributes:
        ID: ``0x78337739``

    Args:
        order: List of ``int`` ``64-bit``
        masks (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x78337739

    def __init__(self, order: list, masks: bool = None):
        self.masks = masks  # flags.0?true
        self.order = order  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args) -> "ReorderStickerSets":
        flags = Int.read(b)
        
        masks = True if flags & (1 << 0) else False
        order = Object.read(b, Long)
        
        return ReorderStickerSets(order, masks)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.masks is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.order, Long))
        
        return b.getvalue()

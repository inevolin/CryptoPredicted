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


class GetArchivedStickers(Object):
    """Attributes:
        ID: ``0x57f17692``

    Args:
        offset_id: ``int`` ``64-bit``
        limit: ``int`` ``32-bit``
        masks (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`messages.ArchivedStickers <pyrogram.api.types.messages.ArchivedStickers>`
    """

    ID = 0x57f17692

    def __init__(self, offset_id: int, limit: int, masks: bool = None):
        self.masks = masks  # flags.0?true
        self.offset_id = offset_id  # long
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetArchivedStickers":
        flags = Int.read(b)
        
        masks = True if flags & (1 << 0) else False
        offset_id = Long.read(b)
        
        limit = Int.read(b)
        
        return GetArchivedStickers(offset_id, limit, masks)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.masks is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

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


class SaveBigFilePart(Object):
    """Attributes:
        ID: ``0xde7b673d``

    Args:
        file_id: ``int`` ``64-bit``
        file_part: ``int`` ``32-bit``
        file_total_parts: ``int`` ``32-bit``
        bytes: ``bytes``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xde7b673d

    def __init__(self, file_id: int, file_part: int, file_total_parts: int, bytes: bytes):
        self.file_id = file_id  # long
        self.file_part = file_part  # int
        self.file_total_parts = file_total_parts  # int
        self.bytes = bytes  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SaveBigFilePart":
        # No flags
        
        file_id = Long.read(b)
        
        file_part = Int.read(b)
        
        file_total_parts = Int.read(b)
        
        bytes = Bytes.read(b)
        
        return SaveBigFilePart(file_id, file_part, file_total_parts, bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.file_id))
        
        b.write(Int(self.file_part))
        
        b.write(Int(self.file_total_parts))
        
        b.write(Bytes(self.bytes))
        
        return b.getvalue()

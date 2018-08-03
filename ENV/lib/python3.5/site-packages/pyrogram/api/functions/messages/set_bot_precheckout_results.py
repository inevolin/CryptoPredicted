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


class SetBotPrecheckoutResults(Object):
    """Attributes:
        ID: ``0x09c2dd95``

    Args:
        query_id: ``int`` ``64-bit``
        success (optional): ``bool``
        error (optional): ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x09c2dd95

    def __init__(self, query_id: int, success: bool = None, error: str = None):
        self.success = success  # flags.1?true
        self.query_id = query_id  # long
        self.error = error  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args) -> "SetBotPrecheckoutResults":
        flags = Int.read(b)
        
        success = True if flags & (1 << 1) else False
        query_id = Long.read(b)
        
        error = String.read(b) if flags & (1 << 0) else None
        return SetBotPrecheckoutResults(query_id, success, error)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.success is not None else 0
        flags |= (1 << 0) if self.error is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        if self.error is not None:
            b.write(String(self.error))
        
        return b.getvalue()

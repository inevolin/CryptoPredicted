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


class ChannelForbidden(Object):
    """Attributes:
        ID: ``0x289da732``

    Args:
        id: ``int`` ``32-bit``
        access_hash: ``int`` ``64-bit``
        title: ``str``
        broadcast (optional): ``bool``
        megagroup (optional): ``bool``
        until_date (optional): ``int`` ``32-bit``
    """

    ID = 0x289da732

    def __init__(self, id: int, access_hash: int, title: str, broadcast: bool = None, megagroup: bool = None, until_date: int = None):
        self.broadcast = broadcast  # flags.5?true
        self.megagroup = megagroup  # flags.8?true
        self.id = id  # int
        self.access_hash = access_hash  # long
        self.title = title  # string
        self.until_date = until_date  # flags.16?int

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelForbidden":
        flags = Int.read(b)
        
        broadcast = True if flags & (1 << 5) else False
        megagroup = True if flags & (1 << 8) else False
        id = Int.read(b)
        
        access_hash = Long.read(b)
        
        title = String.read(b)
        
        until_date = Int.read(b) if flags & (1 << 16) else None
        return ChannelForbidden(id, access_hash, title, broadcast, megagroup, until_date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 5) if self.broadcast is not None else 0
        flags |= (1 << 8) if self.megagroup is not None else 0
        flags |= (1 << 16) if self.until_date is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(String(self.title))
        
        if self.until_date is not None:
            b.write(Int(self.until_date))
        
        return b.getvalue()

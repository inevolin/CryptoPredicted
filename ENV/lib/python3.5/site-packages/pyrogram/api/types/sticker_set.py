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


class StickerSet(Object):
    """Attributes:
        ID: ``0x5585a139``

    Args:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        title: ``str``
        short_name: ``str``
        count: ``int`` ``32-bit``
        hash: ``int`` ``32-bit``
        archived (optional): ``bool``
        official (optional): ``bool``
        masks (optional): ``bool``
        installed_date (optional): ``int`` ``32-bit``
    """

    ID = 0x5585a139

    def __init__(self, id: int, access_hash: int, title: str, short_name: str, count: int, hash: int, archived: bool = None, official: bool = None, masks: bool = None, installed_date: int = None):
        self.archived = archived  # flags.1?true
        self.official = official  # flags.2?true
        self.masks = masks  # flags.3?true
        self.installed_date = installed_date  # flags.0?int
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.title = title  # string
        self.short_name = short_name  # string
        self.count = count  # int
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "StickerSet":
        flags = Int.read(b)
        
        archived = True if flags & (1 << 1) else False
        official = True if flags & (1 << 2) else False
        masks = True if flags & (1 << 3) else False
        installed_date = Int.read(b) if flags & (1 << 0) else None
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        title = String.read(b)
        
        short_name = String.read(b)
        
        count = Int.read(b)
        
        hash = Int.read(b)
        
        return StickerSet(id, access_hash, title, short_name, count, hash, archived, official, masks, installed_date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.archived is not None else 0
        flags |= (1 << 2) if self.official is not None else 0
        flags |= (1 << 3) if self.masks is not None else 0
        flags |= (1 << 0) if self.installed_date is not None else 0
        b.write(Int(flags))
        
        if self.installed_date is not None:
            b.write(Int(self.installed_date))
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(String(self.title))
        
        b.write(String(self.short_name))
        
        b.write(Int(self.count))
        
        b.write(Int(self.hash))
        
        return b.getvalue()

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


class Chat(Object):
    """Attributes:
        ID: ``0xd91cdd54``

    Args:
        id: ``int`` ``32-bit``
        title: ``str``
        photo: Either :obj:`ChatPhotoEmpty <pyrogram.api.types.ChatPhotoEmpty>` or :obj:`ChatPhoto <pyrogram.api.types.ChatPhoto>`
        participants_count: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        version: ``int`` ``32-bit``
        creator (optional): ``bool``
        kicked (optional): ``bool``
        left (optional): ``bool``
        admins_enabled (optional): ``bool``
        admin (optional): ``bool``
        deactivated (optional): ``bool``
        migrated_to (optional): Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`
    """

    ID = 0xd91cdd54

    def __init__(self, id: int, title: str, photo, participants_count: int, date: int, version: int, creator: bool = None, kicked: bool = None, left: bool = None, admins_enabled: bool = None, admin: bool = None, deactivated: bool = None, migrated_to=None):
        self.creator = creator  # flags.0?true
        self.kicked = kicked  # flags.1?true
        self.left = left  # flags.2?true
        self.admins_enabled = admins_enabled  # flags.3?true
        self.admin = admin  # flags.4?true
        self.deactivated = deactivated  # flags.5?true
        self.id = id  # int
        self.title = title  # string
        self.photo = photo  # ChatPhoto
        self.participants_count = participants_count  # int
        self.date = date  # int
        self.version = version  # int
        self.migrated_to = migrated_to  # flags.6?InputChannel

    @staticmethod
    def read(b: BytesIO, *args) -> "Chat":
        flags = Int.read(b)
        
        creator = True if flags & (1 << 0) else False
        kicked = True if flags & (1 << 1) else False
        left = True if flags & (1 << 2) else False
        admins_enabled = True if flags & (1 << 3) else False
        admin = True if flags & (1 << 4) else False
        deactivated = True if flags & (1 << 5) else False
        id = Int.read(b)
        
        title = String.read(b)
        
        photo = Object.read(b)
        
        participants_count = Int.read(b)
        
        date = Int.read(b)
        
        version = Int.read(b)
        
        migrated_to = Object.read(b) if flags & (1 << 6) else None
        
        return Chat(id, title, photo, participants_count, date, version, creator, kicked, left, admins_enabled, admin, deactivated, migrated_to)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.creator is not None else 0
        flags |= (1 << 1) if self.kicked is not None else 0
        flags |= (1 << 2) if self.left is not None else 0
        flags |= (1 << 3) if self.admins_enabled is not None else 0
        flags |= (1 << 4) if self.admin is not None else 0
        flags |= (1 << 5) if self.deactivated is not None else 0
        flags |= (1 << 6) if self.migrated_to is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(String(self.title))
        
        b.write(self.photo.write())
        
        b.write(Int(self.participants_count))
        
        b.write(Int(self.date))
        
        b.write(Int(self.version))
        
        if self.migrated_to is not None:
            b.write(self.migrated_to.write())
        
        return b.getvalue()

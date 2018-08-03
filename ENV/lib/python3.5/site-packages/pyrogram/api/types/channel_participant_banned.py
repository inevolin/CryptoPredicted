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


class ChannelParticipantBanned(Object):
    """Attributes:
        ID: ``0x222c1886``

    Args:
        user_id: ``int`` ``32-bit``
        kicked_by: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        banned_rights: :obj:`ChannelBannedRights <pyrogram.api.types.ChannelBannedRights>`
        left (optional): ``bool``
    """

    ID = 0x222c1886

    def __init__(self, user_id: int, kicked_by: int, date: int, banned_rights, left: bool = None):
        self.left = left  # flags.0?true
        self.user_id = user_id  # int
        self.kicked_by = kicked_by  # int
        self.date = date  # int
        self.banned_rights = banned_rights  # ChannelBannedRights

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelParticipantBanned":
        flags = Int.read(b)
        
        left = True if flags & (1 << 0) else False
        user_id = Int.read(b)
        
        kicked_by = Int.read(b)
        
        date = Int.read(b)
        
        banned_rights = Object.read(b)
        
        return ChannelParticipantBanned(user_id, kicked_by, date, banned_rights, left)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.left is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.user_id))
        
        b.write(Int(self.kicked_by))
        
        b.write(Int(self.date))
        
        b.write(self.banned_rights.write())
        
        return b.getvalue()

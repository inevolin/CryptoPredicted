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


class ChannelParticipantAdmin(Object):
    """Attributes:
        ID: ``0xa82fa898``

    Args:
        user_id: ``int`` ``32-bit``
        inviter_id: ``int`` ``32-bit``
        promoted_by: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
        admin_rights: :obj:`ChannelAdminRights <pyrogram.api.types.ChannelAdminRights>`
        can_edit (optional): ``bool``
    """

    ID = 0xa82fa898

    def __init__(self, user_id: int, inviter_id: int, promoted_by: int, date: int, admin_rights, can_edit: bool = None):
        self.can_edit = can_edit  # flags.0?true
        self.user_id = user_id  # int
        self.inviter_id = inviter_id  # int
        self.promoted_by = promoted_by  # int
        self.date = date  # int
        self.admin_rights = admin_rights  # ChannelAdminRights

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelParticipantAdmin":
        flags = Int.read(b)
        
        can_edit = True if flags & (1 << 0) else False
        user_id = Int.read(b)
        
        inviter_id = Int.read(b)
        
        promoted_by = Int.read(b)
        
        date = Int.read(b)
        
        admin_rights = Object.read(b)
        
        return ChannelParticipantAdmin(user_id, inviter_id, promoted_by, date, admin_rights, can_edit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.can_edit is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.user_id))
        
        b.write(Int(self.inviter_id))
        
        b.write(Int(self.promoted_by))
        
        b.write(Int(self.date))
        
        b.write(self.admin_rights.write())
        
        return b.getvalue()

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


class ContactStatus(Object):
    """Attributes:
        ID: ``0xd3680c61``

    Args:
        user_id: ``int`` ``32-bit``
        status: Either :obj:`UserStatusEmpty <pyrogram.api.types.UserStatusEmpty>`, :obj:`UserStatusOnline <pyrogram.api.types.UserStatusOnline>`, :obj:`UserStatusOffline <pyrogram.api.types.UserStatusOffline>`, :obj:`UserStatusRecently <pyrogram.api.types.UserStatusRecently>`, :obj:`UserStatusLastWeek <pyrogram.api.types.UserStatusLastWeek>` or :obj:`UserStatusLastMonth <pyrogram.api.types.UserStatusLastMonth>`

    See Also:
        This object can be returned by :obj:`contacts.GetStatuses <pyrogram.api.functions.contacts.GetStatuses>`.
    """

    ID = 0xd3680c61

    def __init__(self, user_id: int, status):
        self.user_id = user_id  # int
        self.status = status  # UserStatus

    @staticmethod
    def read(b: BytesIO, *args) -> "ContactStatus":
        # No flags
        
        user_id = Int.read(b)
        
        status = Object.read(b)
        
        return ContactStatus(user_id, status)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(self.status.write())
        
        return b.getvalue()

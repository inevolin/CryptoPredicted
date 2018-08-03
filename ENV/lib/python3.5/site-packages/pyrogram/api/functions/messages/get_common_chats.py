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


class GetCommonChats(Object):
    """Attributes:
        ID: ``0x0d0a48c4``

    Args:
        user_id: Either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>` or :obj:`InputUser <pyrogram.api.types.InputUser>`
        max_id: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.Chats <pyrogram.api.types.messages.Chats>` or :obj:`messages.ChatsSlice <pyrogram.api.types.messages.ChatsSlice>`
    """

    ID = 0x0d0a48c4

    def __init__(self, user_id, max_id: int, limit: int):
        self.user_id = user_id  # InputUser
        self.max_id = max_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetCommonChats":
        # No flags
        
        user_id = Object.read(b)
        
        max_id = Int.read(b)
        
        limit = Int.read(b)
        
        return GetCommonChats(user_id, max_id, limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.user_id.write())
        
        b.write(Int(self.max_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

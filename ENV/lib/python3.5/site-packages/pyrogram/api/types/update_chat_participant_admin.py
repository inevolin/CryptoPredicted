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


class UpdateChatParticipantAdmin(Object):
    """Attributes:
        ID: ``0xb6901959``

    Args:
        chat_id: ``int`` ``32-bit``
        user_id: ``int`` ``32-bit``
        is_admin: ``bool``
        version: ``int`` ``32-bit``
    """

    ID = 0xb6901959

    def __init__(self, chat_id: int, user_id: int, is_admin: bool, version: int):
        self.chat_id = chat_id  # int
        self.user_id = user_id  # int
        self.is_admin = is_admin  # Bool
        self.version = version  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateChatParticipantAdmin":
        # No flags
        
        chat_id = Int.read(b)
        
        user_id = Int.read(b)
        
        is_admin = Bool.read(b)
        
        version = Int.read(b)
        
        return UpdateChatParticipantAdmin(chat_id, user_id, is_admin, version)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(Int(self.user_id))
        
        b.write(Bool(self.is_admin))
        
        b.write(Int(self.version))
        
        return b.getvalue()

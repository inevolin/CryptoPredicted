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


class ChatParticipants(Object):
    """Attributes:
        ID: ``0x3f460fed``

    Args:
        chat_id: ``int`` ``32-bit``
        participants: List of either :obj:`ChatParticipant <pyrogram.api.types.ChatParticipant>`, :obj:`ChatParticipantCreator <pyrogram.api.types.ChatParticipantCreator>` or :obj:`ChatParticipantAdmin <pyrogram.api.types.ChatParticipantAdmin>`
        version: ``int`` ``32-bit``
    """

    ID = 0x3f460fed

    def __init__(self, chat_id: int, participants: list, version: int):
        self.chat_id = chat_id  # int
        self.participants = participants  # Vector<ChatParticipant>
        self.version = version  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatParticipants":
        # No flags
        
        chat_id = Int.read(b)
        
        participants = Object.read(b)
        
        version = Int.read(b)
        
        return ChatParticipants(chat_id, participants, version)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(Vector(self.participants))
        
        b.write(Int(self.version))
        
        return b.getvalue()

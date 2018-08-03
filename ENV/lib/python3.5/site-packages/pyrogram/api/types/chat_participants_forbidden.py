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


class ChatParticipantsForbidden(Object):
    """Attributes:
        ID: ``0xfc900c2b``

    Args:
        chat_id: ``int`` ``32-bit``
        self_participant (optional): Either :obj:`ChatParticipant <pyrogram.api.types.ChatParticipant>`, :obj:`ChatParticipantCreator <pyrogram.api.types.ChatParticipantCreator>` or :obj:`ChatParticipantAdmin <pyrogram.api.types.ChatParticipantAdmin>`
    """

    ID = 0xfc900c2b

    def __init__(self, chat_id: int, self_participant=None):
        self.chat_id = chat_id  # int
        self.self_participant = self_participant  # flags.0?ChatParticipant

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatParticipantsForbidden":
        flags = Int.read(b)
        
        chat_id = Int.read(b)
        
        self_participant = Object.read(b) if flags & (1 << 0) else None
        
        return ChatParticipantsForbidden(chat_id, self_participant)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.self_participant is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.chat_id))
        
        if self.self_participant is not None:
            b.write(self.self_participant.write())
        
        return b.getvalue()

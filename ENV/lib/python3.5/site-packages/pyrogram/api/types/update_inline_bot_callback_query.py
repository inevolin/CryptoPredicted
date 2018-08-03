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


class UpdateInlineBotCallbackQuery(Object):
    """Attributes:
        ID: ``0xf9d27a5a``

    Args:
        query_id: ``int`` ``64-bit``
        user_id: ``int`` ``32-bit``
        msg_id: :obj:`InputBotInlineMessageID <pyrogram.api.types.InputBotInlineMessageID>`
        chat_instance: ``int`` ``64-bit``
        data (optional): ``bytes``
        game_short_name (optional): ``str``
    """

    ID = 0xf9d27a5a

    def __init__(self, query_id: int, user_id: int, msg_id, chat_instance: int, data: bytes = None, game_short_name: str = None):
        self.query_id = query_id  # long
        self.user_id = user_id  # int
        self.msg_id = msg_id  # InputBotInlineMessageID
        self.chat_instance = chat_instance  # long
        self.data = data  # flags.0?bytes
        self.game_short_name = game_short_name  # flags.1?string

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateInlineBotCallbackQuery":
        flags = Int.read(b)
        
        query_id = Long.read(b)
        
        user_id = Int.read(b)
        
        msg_id = Object.read(b)
        
        chat_instance = Long.read(b)
        
        data = Bytes.read(b) if flags & (1 << 0) else None
        game_short_name = String.read(b) if flags & (1 << 1) else None
        return UpdateInlineBotCallbackQuery(query_id, user_id, msg_id, chat_instance, data, game_short_name)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.data is not None else 0
        flags |= (1 << 1) if self.game_short_name is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        b.write(Int(self.user_id))
        
        b.write(self.msg_id.write())
        
        b.write(Long(self.chat_instance))
        
        if self.data is not None:
            b.write(Bytes(self.data))
        
        if self.game_short_name is not None:
            b.write(String(self.game_short_name))
        
        return b.getvalue()

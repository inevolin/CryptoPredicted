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


class ChannelMessages(Object):
    """Attributes:
        ID: ``0x99262e37``

    Args:
        pts: ``int`` ``32-bit``
        count: ``int`` ``32-bit``
        messages: List of either :obj:`MessageEmpty <pyrogram.api.types.MessageEmpty>`, :obj:`Message <pyrogram.api.types.Message>` or :obj:`MessageService <pyrogram.api.types.MessageService>`
        chats: List of either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`messages.GetMessages <pyrogram.api.functions.messages.GetMessages>`, :obj:`messages.GetHistory <pyrogram.api.functions.messages.GetHistory>`, :obj:`messages.Search <pyrogram.api.functions.messages.Search>`, :obj:`messages.SearchGlobal <pyrogram.api.functions.messages.SearchGlobal>`, :obj:`messages.GetUnreadMentions <pyrogram.api.functions.messages.GetUnreadMentions>`, :obj:`messages.GetRecentLocations <pyrogram.api.functions.messages.GetRecentLocations>` and :obj:`channels.GetMessages <pyrogram.api.functions.channels.GetMessages>`.
    """

    ID = 0x99262e37

    def __init__(self, pts: int, count: int, messages: list, chats: list, users: list):
        self.pts = pts  # int
        self.count = count  # int
        self.messages = messages  # Vector<Message>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelMessages":
        flags = Int.read(b)
        
        pts = Int.read(b)
        
        count = Int.read(b)
        
        messages = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return ChannelMessages(pts, count, messages, chats, users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        
        b.write(Int(flags))
        
        b.write(Int(self.pts))
        
        b.write(Int(self.count))
        
        b.write(Vector(self.messages))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()

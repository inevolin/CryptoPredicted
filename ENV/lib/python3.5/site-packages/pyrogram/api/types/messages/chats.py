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


class Chats(Object):
    """Attributes:
        ID: ``0x64ff9fd5``

    Args:
        chats: List of either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`

    See Also:
        This object can be returned by :obj:`messages.GetChats <pyrogram.api.functions.messages.GetChats>`, :obj:`messages.GetCommonChats <pyrogram.api.functions.messages.GetCommonChats>`, :obj:`messages.GetAllChats <pyrogram.api.functions.messages.GetAllChats>`, :obj:`channels.GetChannels <pyrogram.api.functions.channels.GetChannels>` and :obj:`channels.GetAdminedPublicChannels <pyrogram.api.functions.channels.GetAdminedPublicChannels>`.
    """

    ID = 0x64ff9fd5

    def __init__(self, chats: list):
        self.chats = chats  # Vector<Chat>

    @staticmethod
    def read(b: BytesIO, *args) -> "Chats":
        # No flags
        
        chats = Object.read(b)
        
        return Chats(chats)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.chats))
        
        return b.getvalue()

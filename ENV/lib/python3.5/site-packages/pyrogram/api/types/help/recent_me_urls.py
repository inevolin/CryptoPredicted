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


class RecentMeUrls(Object):
    """Attributes:
        ID: ``0x0e0310d7``

    Args:
        urls: List of either :obj:`RecentMeUrlUnknown <pyrogram.api.types.RecentMeUrlUnknown>`, :obj:`RecentMeUrlUser <pyrogram.api.types.RecentMeUrlUser>`, :obj:`RecentMeUrlChat <pyrogram.api.types.RecentMeUrlChat>`, :obj:`RecentMeUrlChatInvite <pyrogram.api.types.RecentMeUrlChatInvite>` or :obj:`RecentMeUrlStickerSet <pyrogram.api.types.RecentMeUrlStickerSet>`
        chats: List of either :obj:`ChatEmpty <pyrogram.api.types.ChatEmpty>`, :obj:`Chat <pyrogram.api.types.Chat>`, :obj:`ChatForbidden <pyrogram.api.types.ChatForbidden>`, :obj:`Channel <pyrogram.api.types.Channel>` or :obj:`ChannelForbidden <pyrogram.api.types.ChannelForbidden>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`help.GetRecentMeUrls <pyrogram.api.functions.help.GetRecentMeUrls>`.
    """

    ID = 0x0e0310d7

    def __init__(self, urls: list, chats: list, users: list):
        self.urls = urls  # Vector<RecentMeUrl>
        self.chats = chats  # Vector<Chat>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "RecentMeUrls":
        # No flags
        
        urls = Object.read(b)
        
        chats = Object.read(b)
        
        users = Object.read(b)
        
        return RecentMeUrls(urls, chats, users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.urls))
        
        b.write(Vector(self.chats))
        
        b.write(Vector(self.users))
        
        return b.getvalue()

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


class RecentMeUrlChatInvite(Object):
    """Attributes:
        ID: ``0xeb49081d``

    Args:
        url: ``str``
        chat_invite: Either :obj:`ChatInviteAlready <pyrogram.api.types.ChatInviteAlready>` or :obj:`ChatInvite <pyrogram.api.types.ChatInvite>`
    """

    ID = 0xeb49081d

    def __init__(self, url: str, chat_invite):
        self.url = url  # string
        self.chat_invite = chat_invite  # ChatInvite

    @staticmethod
    def read(b: BytesIO, *args) -> "RecentMeUrlChatInvite":
        # No flags
        
        url = String.read(b)
        
        chat_invite = Object.read(b)
        
        return RecentMeUrlChatInvite(url, chat_invite)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(self.chat_invite.write())
        
        return b.getvalue()

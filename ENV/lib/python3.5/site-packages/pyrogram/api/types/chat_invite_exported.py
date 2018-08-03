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


class ChatInviteExported(Object):
    """Attributes:
        ID: ``0xfc2e05bc``

    Args:
        link: ``str``

    See Also:
        This object can be returned by :obj:`messages.ExportChatInvite <pyrogram.api.functions.messages.ExportChatInvite>` and :obj:`channels.ExportInvite <pyrogram.api.functions.channels.ExportInvite>`.
    """

    ID = 0xfc2e05bc

    def __init__(self, link: str):
        self.link = link  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatInviteExported":
        # No flags
        
        link = String.read(b)
        
        return ChatInviteExported(link)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.link))
        
        return b.getvalue()

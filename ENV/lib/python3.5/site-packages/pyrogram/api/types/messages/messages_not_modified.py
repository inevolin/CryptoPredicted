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


class MessagesNotModified(Object):
    """Attributes:
        ID: ``0x74535f21``

    Args:
        count: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.GetMessages <pyrogram.api.functions.messages.GetMessages>`, :obj:`messages.GetHistory <pyrogram.api.functions.messages.GetHistory>`, :obj:`messages.Search <pyrogram.api.functions.messages.Search>`, :obj:`messages.SearchGlobal <pyrogram.api.functions.messages.SearchGlobal>`, :obj:`messages.GetUnreadMentions <pyrogram.api.functions.messages.GetUnreadMentions>`, :obj:`messages.GetRecentLocations <pyrogram.api.functions.messages.GetRecentLocations>` and :obj:`channels.GetMessages <pyrogram.api.functions.channels.GetMessages>`.
    """

    ID = 0x74535f21

    def __init__(self, count: int):
        self.count = count  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "MessagesNotModified":
        # No flags
        
        count = Int.read(b)
        
        return MessagesNotModified(count)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        return b.getvalue()

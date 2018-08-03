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


class BotResults(Object):
    """Attributes:
        ID: ``0x947ca848``

    Args:
        query_id: ``int`` ``64-bit``
        results: List of either :obj:`BotInlineResult <pyrogram.api.types.BotInlineResult>` or :obj:`BotInlineMediaResult <pyrogram.api.types.BotInlineMediaResult>`
        cache_time: ``int`` ``32-bit``
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`
        gallery (optional): ``bool``
        next_offset (optional): ``str``
        switch_pm (optional): :obj:`InlineBotSwitchPM <pyrogram.api.types.InlineBotSwitchPM>`

    See Also:
        This object can be returned by :obj:`messages.GetInlineBotResults <pyrogram.api.functions.messages.GetInlineBotResults>`.
    """

    ID = 0x947ca848

    def __init__(self, query_id: int, results: list, cache_time: int, users: list, gallery: bool = None, next_offset: str = None, switch_pm=None):
        self.gallery = gallery  # flags.0?true
        self.query_id = query_id  # long
        self.next_offset = next_offset  # flags.1?string
        self.switch_pm = switch_pm  # flags.2?InlineBotSwitchPM
        self.results = results  # Vector<BotInlineResult>
        self.cache_time = cache_time  # int
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "BotResults":
        flags = Int.read(b)
        
        gallery = True if flags & (1 << 0) else False
        query_id = Long.read(b)
        
        next_offset = String.read(b) if flags & (1 << 1) else None
        switch_pm = Object.read(b) if flags & (1 << 2) else None
        
        results = Object.read(b)
        
        cache_time = Int.read(b)
        
        users = Object.read(b)
        
        return BotResults(query_id, results, cache_time, users, gallery, next_offset, switch_pm)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.gallery is not None else 0
        flags |= (1 << 1) if self.next_offset is not None else 0
        flags |= (1 << 2) if self.switch_pm is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        if self.switch_pm is not None:
            b.write(self.switch_pm.write())
        
        b.write(Vector(self.results))
        
        b.write(Int(self.cache_time))
        
        b.write(Vector(self.users))
        
        return b.getvalue()

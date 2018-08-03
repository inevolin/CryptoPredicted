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


class SetInlineBotResults(Object):
    """Attributes:
        ID: ``0xeb5ea206``

    Args:
        query_id: ``int`` ``64-bit``
        results: List of either :obj:`InputBotInlineResult <pyrogram.api.types.InputBotInlineResult>`, :obj:`InputBotInlineResultPhoto <pyrogram.api.types.InputBotInlineResultPhoto>`, :obj:`InputBotInlineResultDocument <pyrogram.api.types.InputBotInlineResultDocument>` or :obj:`InputBotInlineResultGame <pyrogram.api.types.InputBotInlineResultGame>`
        cache_time: ``int`` ``32-bit``
        gallery (optional): ``bool``
        private (optional): ``bool``
        next_offset (optional): ``str``
        switch_pm (optional): :obj:`InlineBotSwitchPM <pyrogram.api.types.InlineBotSwitchPM>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xeb5ea206

    def __init__(self, query_id: int, results: list, cache_time: int, gallery: bool = None, private: bool = None, next_offset: str = None, switch_pm=None):
        self.gallery = gallery  # flags.0?true
        self.private = private  # flags.1?true
        self.query_id = query_id  # long
        self.results = results  # Vector<InputBotInlineResult>
        self.cache_time = cache_time  # int
        self.next_offset = next_offset  # flags.2?string
        self.switch_pm = switch_pm  # flags.3?InlineBotSwitchPM

    @staticmethod
    def read(b: BytesIO, *args) -> "SetInlineBotResults":
        flags = Int.read(b)
        
        gallery = True if flags & (1 << 0) else False
        private = True if flags & (1 << 1) else False
        query_id = Long.read(b)
        
        results = Object.read(b)
        
        cache_time = Int.read(b)
        
        next_offset = String.read(b) if flags & (1 << 2) else None
        switch_pm = Object.read(b) if flags & (1 << 3) else None
        
        return SetInlineBotResults(query_id, results, cache_time, gallery, private, next_offset, switch_pm)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.gallery is not None else 0
        flags |= (1 << 1) if self.private is not None else 0
        flags |= (1 << 2) if self.next_offset is not None else 0
        flags |= (1 << 3) if self.switch_pm is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.query_id))
        
        b.write(Vector(self.results))
        
        b.write(Int(self.cache_time))
        
        if self.next_offset is not None:
            b.write(String(self.next_offset))
        
        if self.switch_pm is not None:
            b.write(self.switch_pm.write())
        
        return b.getvalue()

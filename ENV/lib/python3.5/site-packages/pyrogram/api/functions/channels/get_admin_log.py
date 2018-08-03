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


class GetAdminLog(Object):
    """Attributes:
        ID: ``0x33ddf480``

    Args:
        channel: Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`
        q: ``str``
        max_id: ``int`` ``64-bit``
        min_id: ``int`` ``64-bit``
        limit: ``int`` ``32-bit``
        events_filter (optional): :obj:`ChannelAdminLogEventsFilter <pyrogram.api.types.ChannelAdminLogEventsFilter>`
        admins (optional): List of either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>` or :obj:`InputUser <pyrogram.api.types.InputUser>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`channels.AdminLogResults <pyrogram.api.types.channels.AdminLogResults>`
    """

    ID = 0x33ddf480

    def __init__(self, channel, q: str, max_id: int, min_id: int, limit: int, events_filter=None, admins: list = None):
        self.channel = channel  # InputChannel
        self.q = q  # string
        self.events_filter = events_filter  # flags.0?ChannelAdminLogEventsFilter
        self.admins = admins  # flags.1?Vector<InputUser>
        self.max_id = max_id  # long
        self.min_id = min_id  # long
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetAdminLog":
        flags = Int.read(b)
        
        channel = Object.read(b)
        
        q = String.read(b)
        
        events_filter = Object.read(b) if flags & (1 << 0) else None
        
        admins = Object.read(b) if flags & (1 << 1) else []
        
        max_id = Long.read(b)
        
        min_id = Long.read(b)
        
        limit = Int.read(b)
        
        return GetAdminLog(channel, q, max_id, min_id, limit, events_filter, admins)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.events_filter is not None else 0
        flags |= (1 << 1) if self.admins is not None else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        b.write(String(self.q))
        
        if self.events_filter is not None:
            b.write(self.events_filter.write())
        
        if self.admins is not None:
            b.write(Vector(self.admins))
        
        b.write(Long(self.max_id))
        
        b.write(Long(self.min_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

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


class GetChannelDifference(Object):
    """Attributes:
        ID: ``0x03173d78``

    Args:
        channel: Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`
        filter: Either :obj:`ChannelMessagesFilterEmpty <pyrogram.api.types.ChannelMessagesFilterEmpty>` or :obj:`ChannelMessagesFilter <pyrogram.api.types.ChannelMessagesFilter>`
        pts: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``
        force (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`updates.ChannelDifferenceEmpty <pyrogram.api.types.updates.ChannelDifferenceEmpty>`, :obj:`updates.ChannelDifferenceTooLong <pyrogram.api.types.updates.ChannelDifferenceTooLong>` or :obj:`updates.ChannelDifference <pyrogram.api.types.updates.ChannelDifference>`
    """

    ID = 0x03173d78

    def __init__(self, channel, filter, pts: int, limit: int, force: bool = None):
        self.force = force  # flags.0?true
        self.channel = channel  # InputChannel
        self.filter = filter  # ChannelMessagesFilter
        self.pts = pts  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetChannelDifference":
        flags = Int.read(b)
        
        force = True if flags & (1 << 0) else False
        channel = Object.read(b)
        
        filter = Object.read(b)
        
        pts = Int.read(b)
        
        limit = Int.read(b)
        
        return GetChannelDifference(channel, filter, pts, limit, force)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.force is not None else 0
        b.write(Int(flags))
        
        b.write(self.channel.write())
        
        b.write(self.filter.write())
        
        b.write(Int(self.pts))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

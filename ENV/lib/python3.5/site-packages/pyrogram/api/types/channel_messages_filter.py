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


class ChannelMessagesFilter(Object):
    """Attributes:
        ID: ``0xcd77d957``

    Args:
        ranges: List of :obj:`MessageRange <pyrogram.api.types.MessageRange>`
        exclude_new_messages (optional): ``bool``
    """

    ID = 0xcd77d957

    def __init__(self, ranges: list, exclude_new_messages: bool = None):
        self.exclude_new_messages = exclude_new_messages  # flags.1?true
        self.ranges = ranges  # Vector<MessageRange>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelMessagesFilter":
        flags = Int.read(b)
        
        exclude_new_messages = True if flags & (1 << 1) else False
        ranges = Object.read(b)
        
        return ChannelMessagesFilter(ranges, exclude_new_messages)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.exclude_new_messages is not None else 0
        b.write(Int(flags))
        
        b.write(Vector(self.ranges))
        
        return b.getvalue()

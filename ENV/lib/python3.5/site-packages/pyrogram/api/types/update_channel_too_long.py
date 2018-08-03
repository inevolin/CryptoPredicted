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


class UpdateChannelTooLong(Object):
    """Attributes:
        ID: ``0xeb0467fb``

    Args:
        channel_id: ``int`` ``32-bit``
        pts (optional): ``int`` ``32-bit``
    """

    ID = 0xeb0467fb

    def __init__(self, channel_id: int, pts: int = None):
        self.channel_id = channel_id  # int
        self.pts = pts  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateChannelTooLong":
        flags = Int.read(b)
        
        channel_id = Int.read(b)
        
        pts = Int.read(b) if flags & (1 << 0) else None
        return UpdateChannelTooLong(channel_id, pts)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.pts is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.channel_id))
        
        if self.pts is not None:
            b.write(Int(self.pts))
        
        return b.getvalue()

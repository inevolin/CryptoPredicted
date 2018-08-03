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


class UpdateReadChannelOutbox(Object):
    """Attributes:
        ID: ``0x25d6c9c7``

    Args:
        channel_id: ``int`` ``32-bit``
        max_id: ``int`` ``32-bit``
    """

    ID = 0x25d6c9c7

    def __init__(self, channel_id: int, max_id: int):
        self.channel_id = channel_id  # int
        self.max_id = max_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateReadChannelOutbox":
        # No flags
        
        channel_id = Int.read(b)
        
        max_id = Int.read(b)
        
        return UpdateReadChannelOutbox(channel_id, max_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.channel_id))
        
        b.write(Int(self.max_id))
        
        return b.getvalue()

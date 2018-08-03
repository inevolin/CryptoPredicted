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


class ReadMessageContents(Object):
    """Attributes:
        ID: ``0xeab5dc38``

    Args:
        channel: Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`
        id: List of ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xeab5dc38

    def __init__(self, channel, id: list):
        self.channel = channel  # InputChannel
        self.id = id  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args) -> "ReadMessageContents":
        # No flags
        
        channel = Object.read(b)
        
        id = Object.read(b, Int)
        
        return ReadMessageContents(channel, id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Vector(self.id, Int))
        
        return b.getvalue()

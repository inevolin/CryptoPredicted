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


class ExportMessageLink(Object):
    """Attributes:
        ID: ``0xceb77163``

    Args:
        channel: Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`
        id: ``int`` ``32-bit``
        grouped: ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`ExportedMessageLink <pyrogram.api.types.ExportedMessageLink>`
    """

    ID = 0xceb77163

    def __init__(self, channel, id: int, grouped: bool):
        self.channel = channel  # InputChannel
        self.id = id  # int
        self.grouped = grouped  # Bool

    @staticmethod
    def read(b: BytesIO, *args) -> "ExportMessageLink":
        # No flags
        
        channel = Object.read(b)
        
        id = Int.read(b)
        
        grouped = Bool.read(b)
        
        return ExportMessageLink(channel, id, grouped)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.id))
        
        b.write(Bool(self.grouped))
        
        return b.getvalue()

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


class GetChannels(Object):
    """Attributes:
        ID: ``0x0a7f6bbb``

    Args:
        id: List of either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.Chats <pyrogram.api.types.messages.Chats>` or :obj:`messages.ChatsSlice <pyrogram.api.types.messages.ChatsSlice>`
    """

    ID = 0x0a7f6bbb

    def __init__(self, id: list):
        self.id = id  # Vector<InputChannel>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetChannels":
        # No flags
        
        id = Object.read(b)
        
        return GetChannels(id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id))
        
        return b.getvalue()

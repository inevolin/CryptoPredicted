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


class ChannelParticipants(Object):
    """Attributes:
        ID: ``0xf56ee2a8``

    Args:
        count: ``int`` ``32-bit``
        participants: List of either :obj:`ChannelParticipant <pyrogram.api.types.ChannelParticipant>`, :obj:`ChannelParticipantSelf <pyrogram.api.types.ChannelParticipantSelf>`, :obj:`ChannelParticipantCreator <pyrogram.api.types.ChannelParticipantCreator>`, :obj:`ChannelParticipantAdmin <pyrogram.api.types.ChannelParticipantAdmin>` or :obj:`ChannelParticipantBanned <pyrogram.api.types.ChannelParticipantBanned>`
        users: List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`channels.GetParticipants <pyrogram.api.functions.channels.GetParticipants>`.
    """

    ID = 0xf56ee2a8

    def __init__(self, count: int, participants: list, users: list):
        self.count = count  # int
        self.participants = participants  # Vector<ChannelParticipant>
        self.users = users  # Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelParticipants":
        # No flags
        
        count = Int.read(b)
        
        participants = Object.read(b)
        
        users = Object.read(b)
        
        return ChannelParticipants(count, participants, users)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.participants))
        
        b.write(Vector(self.users))
        
        return b.getvalue()

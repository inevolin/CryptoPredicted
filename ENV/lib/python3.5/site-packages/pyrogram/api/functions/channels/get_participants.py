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


class GetParticipants(Object):
    """Attributes:
        ID: ``0x123e05e9``

    Args:
        channel: Either :obj:`InputChannelEmpty <pyrogram.api.types.InputChannelEmpty>` or :obj:`InputChannel <pyrogram.api.types.InputChannel>`
        filter: Either :obj:`ChannelParticipantsRecent <pyrogram.api.types.ChannelParticipantsRecent>`, :obj:`ChannelParticipantsAdmins <pyrogram.api.types.ChannelParticipantsAdmins>`, :obj:`ChannelParticipantsKicked <pyrogram.api.types.ChannelParticipantsKicked>`, :obj:`ChannelParticipantsBots <pyrogram.api.types.ChannelParticipantsBots>`, :obj:`ChannelParticipantsBanned <pyrogram.api.types.ChannelParticipantsBanned>` or :obj:`ChannelParticipantsSearch <pyrogram.api.types.ChannelParticipantsSearch>`
        offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``
        hash: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`channels.ChannelParticipants <pyrogram.api.types.channels.ChannelParticipants>` or :obj:`channels.ChannelParticipantsNotModified <pyrogram.api.types.channels.ChannelParticipantsNotModified>`
    """

    ID = 0x123e05e9

    def __init__(self, channel, filter, offset: int, limit: int, hash: int):
        self.channel = channel  # InputChannel
        self.filter = filter  # ChannelParticipantsFilter
        self.offset = offset  # int
        self.limit = limit  # int
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetParticipants":
        # No flags
        
        channel = Object.read(b)
        
        filter = Object.read(b)
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        hash = Int.read(b)
        
        return GetParticipants(channel, filter, offset, limit, hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(self.filter.write())
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        b.write(Int(self.hash))
        
        return b.getvalue()

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


class ChannelAdminLogEventActionParticipantToggleBan(Object):
    """Attributes:
        ID: ``0xe6d83d7e``

    Args:
        prev_participant: Either :obj:`ChannelParticipant <pyrogram.api.types.ChannelParticipant>`, :obj:`ChannelParticipantSelf <pyrogram.api.types.ChannelParticipantSelf>`, :obj:`ChannelParticipantCreator <pyrogram.api.types.ChannelParticipantCreator>`, :obj:`ChannelParticipantAdmin <pyrogram.api.types.ChannelParticipantAdmin>` or :obj:`ChannelParticipantBanned <pyrogram.api.types.ChannelParticipantBanned>`
        new_participant: Either :obj:`ChannelParticipant <pyrogram.api.types.ChannelParticipant>`, :obj:`ChannelParticipantSelf <pyrogram.api.types.ChannelParticipantSelf>`, :obj:`ChannelParticipantCreator <pyrogram.api.types.ChannelParticipantCreator>`, :obj:`ChannelParticipantAdmin <pyrogram.api.types.ChannelParticipantAdmin>` or :obj:`ChannelParticipantBanned <pyrogram.api.types.ChannelParticipantBanned>`
    """

    ID = 0xe6d83d7e

    def __init__(self, prev_participant, new_participant):
        self.prev_participant = prev_participant  # ChannelParticipant
        self.new_participant = new_participant  # ChannelParticipant

    @staticmethod
    def read(b: BytesIO, *args) -> "ChannelAdminLogEventActionParticipantToggleBan":
        # No flags
        
        prev_participant = Object.read(b)
        
        new_participant = Object.read(b)
        
        return ChannelAdminLogEventActionParticipantToggleBan(prev_participant, new_participant)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.prev_participant.write())
        
        b.write(self.new_participant.write())
        
        return b.getvalue()

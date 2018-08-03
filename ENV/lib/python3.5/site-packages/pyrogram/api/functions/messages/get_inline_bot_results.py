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


class GetInlineBotResults(Object):
    """Attributes:
        ID: ``0x514e999d``

    Args:
        bot: Either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>` or :obj:`InputUser <pyrogram.api.types.InputUser>`
        peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        query: ``str``
        offset: ``str``
        geo_point (optional): Either :obj:`InputGeoPointEmpty <pyrogram.api.types.InputGeoPointEmpty>` or :obj:`InputGeoPoint <pyrogram.api.types.InputGeoPoint>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`messages.BotResults <pyrogram.api.types.messages.BotResults>`
    """

    ID = 0x514e999d

    def __init__(self, bot, peer, query: str, offset: str, geo_point=None):
        self.bot = bot  # InputUser
        self.peer = peer  # InputPeer
        self.geo_point = geo_point  # flags.0?InputGeoPoint
        self.query = query  # string
        self.offset = offset  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "GetInlineBotResults":
        flags = Int.read(b)
        
        bot = Object.read(b)
        
        peer = Object.read(b)
        
        geo_point = Object.read(b) if flags & (1 << 0) else None
        
        query = String.read(b)
        
        offset = String.read(b)
        
        return GetInlineBotResults(bot, peer, query, offset, geo_point)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.geo_point is not None else 0
        b.write(Int(flags))
        
        b.write(self.bot.write())
        
        b.write(self.peer.write())
        
        if self.geo_point is not None:
            b.write(self.geo_point.write())
        
        b.write(String(self.query))
        
        b.write(String(self.offset))
        
        return b.getvalue()

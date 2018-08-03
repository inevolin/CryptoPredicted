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


class SearchGlobal(Object):
    """Attributes:
        ID: ``0x9e3cacb0``

    Args:
        q: ``str``
        offset_date: ``int`` ``32-bit``
        offset_peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        offset_id: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.Messages <pyrogram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <pyrogram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <pyrogram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <pyrogram.api.types.messages.MessagesNotModified>`
    """

    ID = 0x9e3cacb0

    def __init__(self, q: str, offset_date: int, offset_peer, offset_id: int, limit: int):
        self.q = q  # string
        self.offset_date = offset_date  # int
        self.offset_peer = offset_peer  # InputPeer
        self.offset_id = offset_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SearchGlobal":
        # No flags
        
        q = String.read(b)
        
        offset_date = Int.read(b)
        
        offset_peer = Object.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return SearchGlobal(q, offset_date, offset_peer, offset_id, limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        b.write(Int(self.offset_date))
        
        b.write(self.offset_peer.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

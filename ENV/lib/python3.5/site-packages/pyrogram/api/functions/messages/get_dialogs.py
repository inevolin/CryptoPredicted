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


class GetDialogs(Object):
    """Attributes:
        ID: ``0x191ba9c5``

    Args:
        offset_date: ``int`` ``32-bit``
        offset_id: ``int`` ``32-bit``
        offset_peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        limit: ``int`` ``32-bit``
        exclude_pinned (optional): ``bool``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.Dialogs <pyrogram.api.types.messages.Dialogs>` or :obj:`messages.DialogsSlice <pyrogram.api.types.messages.DialogsSlice>`
    """

    ID = 0x191ba9c5

    def __init__(self, offset_date: int, offset_id: int, offset_peer, limit: int, exclude_pinned: bool = None):
        self.exclude_pinned = exclude_pinned  # flags.0?true
        self.offset_date = offset_date  # int
        self.offset_id = offset_id  # int
        self.offset_peer = offset_peer  # InputPeer
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetDialogs":
        flags = Int.read(b)
        
        exclude_pinned = True if flags & (1 << 0) else False
        offset_date = Int.read(b)
        
        offset_id = Int.read(b)
        
        offset_peer = Object.read(b)
        
        limit = Int.read(b)
        
        return GetDialogs(offset_date, offset_id, offset_peer, limit, exclude_pinned)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.exclude_pinned is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.offset_date))
        
        b.write(Int(self.offset_id))
        
        b.write(self.offset_peer.write())
        
        b.write(Int(self.limit))
        
        return b.getvalue()

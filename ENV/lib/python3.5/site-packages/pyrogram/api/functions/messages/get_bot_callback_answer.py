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


class GetBotCallbackAnswer(Object):
    """Attributes:
        ID: ``0x810a9fec``

    Args:
        peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        msg_id: ``int`` ``32-bit``
        game (optional): ``bool``
        data (optional): ``bytes``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`messages.BotCallbackAnswer <pyrogram.api.types.messages.BotCallbackAnswer>`
    """

    ID = 0x810a9fec

    def __init__(self, peer, msg_id: int, game: bool = None, data: bytes = None):
        self.game = game  # flags.1?true
        self.peer = peer  # InputPeer
        self.msg_id = msg_id  # int
        self.data = data  # flags.0?bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "GetBotCallbackAnswer":
        flags = Int.read(b)
        
        game = True if flags & (1 << 1) else False
        peer = Object.read(b)
        
        msg_id = Int.read(b)
        
        data = Bytes.read(b) if flags & (1 << 0) else None
        return GetBotCallbackAnswer(peer, msg_id, game, data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.game is not None else 0
        flags |= (1 << 0) if self.data is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.msg_id))
        
        if self.data is not None:
            b.write(Bytes(self.data))
        
        return b.getvalue()

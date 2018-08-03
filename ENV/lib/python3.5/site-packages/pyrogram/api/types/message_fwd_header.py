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


class MessageFwdHeader(Object):
    """Attributes:
        ID: ``0x559ebe6d``

    Args:
        date: ``int`` ``32-bit``
        from_id (optional): ``int`` ``32-bit``
        channel_id (optional): ``int`` ``32-bit``
        channel_post (optional): ``int`` ``32-bit``
        post_author (optional): ``str``
        saved_from_peer (optional): Either :obj:`PeerUser <pyrogram.api.types.PeerUser>`, :obj:`PeerChat <pyrogram.api.types.PeerChat>` or :obj:`PeerChannel <pyrogram.api.types.PeerChannel>`
        saved_from_msg_id (optional): ``int`` ``32-bit``
    """

    ID = 0x559ebe6d

    def __init__(self, date: int, from_id: int = None, channel_id: int = None, channel_post: int = None, post_author: str = None, saved_from_peer=None, saved_from_msg_id: int = None):
        self.from_id = from_id  # flags.0?int
        self.date = date  # int
        self.channel_id = channel_id  # flags.1?int
        self.channel_post = channel_post  # flags.2?int
        self.post_author = post_author  # flags.3?string
        self.saved_from_peer = saved_from_peer  # flags.4?Peer
        self.saved_from_msg_id = saved_from_msg_id  # flags.4?int

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageFwdHeader":
        flags = Int.read(b)
        
        from_id = Int.read(b) if flags & (1 << 0) else None
        date = Int.read(b)
        
        channel_id = Int.read(b) if flags & (1 << 1) else None
        channel_post = Int.read(b) if flags & (1 << 2) else None
        post_author = String.read(b) if flags & (1 << 3) else None
        saved_from_peer = Object.read(b) if flags & (1 << 4) else None
        
        saved_from_msg_id = Int.read(b) if flags & (1 << 4) else None
        return MessageFwdHeader(date, from_id, channel_id, channel_post, post_author, saved_from_peer, saved_from_msg_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.from_id is not None else 0
        flags |= (1 << 1) if self.channel_id is not None else 0
        flags |= (1 << 2) if self.channel_post is not None else 0
        flags |= (1 << 3) if self.post_author is not None else 0
        flags |= (1 << 4) if self.saved_from_peer is not None else 0
        flags |= (1 << 4) if self.saved_from_msg_id is not None else 0
        b.write(Int(flags))
        
        if self.from_id is not None:
            b.write(Int(self.from_id))
        
        b.write(Int(self.date))
        
        if self.channel_id is not None:
            b.write(Int(self.channel_id))
        
        if self.channel_post is not None:
            b.write(Int(self.channel_post))
        
        if self.post_author is not None:
            b.write(String(self.post_author))
        
        if self.saved_from_peer is not None:
            b.write(self.saved_from_peer.write())
        
        if self.saved_from_msg_id is not None:
            b.write(Int(self.saved_from_msg_id))
        
        return b.getvalue()

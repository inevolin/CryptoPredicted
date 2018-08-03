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


class Search(Object):
    """Attributes:
        ID: ``0x8614ef68``

    Args:
        peer: Either :obj:`InputPeerEmpty <pyrogram.api.types.InputPeerEmpty>`, :obj:`InputPeerSelf <pyrogram.api.types.InputPeerSelf>`, :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>`, :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>`
        q: ``str``
        filter: Either :obj:`InputMessagesFilterEmpty <pyrogram.api.types.InputMessagesFilterEmpty>`, :obj:`InputMessagesFilterPhotos <pyrogram.api.types.InputMessagesFilterPhotos>`, :obj:`InputMessagesFilterVideo <pyrogram.api.types.InputMessagesFilterVideo>`, :obj:`InputMessagesFilterPhotoVideo <pyrogram.api.types.InputMessagesFilterPhotoVideo>`, :obj:`InputMessagesFilterDocument <pyrogram.api.types.InputMessagesFilterDocument>`, :obj:`InputMessagesFilterUrl <pyrogram.api.types.InputMessagesFilterUrl>`, :obj:`InputMessagesFilterGif <pyrogram.api.types.InputMessagesFilterGif>`, :obj:`InputMessagesFilterVoice <pyrogram.api.types.InputMessagesFilterVoice>`, :obj:`InputMessagesFilterMusic <pyrogram.api.types.InputMessagesFilterMusic>`, :obj:`InputMessagesFilterChatPhotos <pyrogram.api.types.InputMessagesFilterChatPhotos>`, :obj:`InputMessagesFilterPhoneCalls <pyrogram.api.types.InputMessagesFilterPhoneCalls>`, :obj:`InputMessagesFilterRoundVoice <pyrogram.api.types.InputMessagesFilterRoundVoice>`, :obj:`InputMessagesFilterRoundVideo <pyrogram.api.types.InputMessagesFilterRoundVideo>`, :obj:`InputMessagesFilterMyMentions <pyrogram.api.types.InputMessagesFilterMyMentions>`, :obj:`InputMessagesFilterGeo <pyrogram.api.types.InputMessagesFilterGeo>` or :obj:`InputMessagesFilterContacts <pyrogram.api.types.InputMessagesFilterContacts>`
        min_date: ``int`` ``32-bit``
        max_date: ``int`` ``32-bit``
        offset_id: ``int`` ``32-bit``
        add_offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``
        max_id: ``int`` ``32-bit``
        min_id: ``int`` ``32-bit``
        hash: ``int`` ``32-bit``
        from_id (optional): Either :obj:`InputUserEmpty <pyrogram.api.types.InputUserEmpty>`, :obj:`InputUserSelf <pyrogram.api.types.InputUserSelf>` or :obj:`InputUser <pyrogram.api.types.InputUser>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.Messages <pyrogram.api.types.messages.Messages>`, :obj:`messages.MessagesSlice <pyrogram.api.types.messages.MessagesSlice>`, :obj:`messages.ChannelMessages <pyrogram.api.types.messages.ChannelMessages>` or :obj:`messages.MessagesNotModified <pyrogram.api.types.messages.MessagesNotModified>`
    """

    ID = 0x8614ef68

    def __init__(self, peer, q: str, filter, min_date: int, max_date: int, offset_id: int, add_offset: int, limit: int, max_id: int, min_id: int, hash: int, from_id=None):
        self.peer = peer  # InputPeer
        self.q = q  # string
        self.from_id = from_id  # flags.0?InputUser
        self.filter = filter  # MessagesFilter
        self.min_date = min_date  # int
        self.max_date = max_date  # int
        self.offset_id = offset_id  # int
        self.add_offset = add_offset  # int
        self.limit = limit  # int
        self.max_id = max_id  # int
        self.min_id = min_id  # int
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "Search":
        flags = Int.read(b)
        
        peer = Object.read(b)
        
        q = String.read(b)
        
        from_id = Object.read(b) if flags & (1 << 0) else None
        
        filter = Object.read(b)
        
        min_date = Int.read(b)
        
        max_date = Int.read(b)
        
        offset_id = Int.read(b)
        
        add_offset = Int.read(b)
        
        limit = Int.read(b)
        
        max_id = Int.read(b)
        
        min_id = Int.read(b)
        
        hash = Int.read(b)
        
        return Search(peer, q, filter, min_date, max_date, offset_id, add_offset, limit, max_id, min_id, hash, from_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.from_id is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(String(self.q))
        
        if self.from_id is not None:
            b.write(self.from_id.write())
        
        b.write(self.filter.write())
        
        b.write(Int(self.min_date))
        
        b.write(Int(self.max_date))
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.add_offset))
        
        b.write(Int(self.limit))
        
        b.write(Int(self.max_id))
        
        b.write(Int(self.min_id))
        
        b.write(Int(self.hash))
        
        return b.getvalue()

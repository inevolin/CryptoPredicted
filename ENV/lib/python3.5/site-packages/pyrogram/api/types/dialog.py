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


class Dialog(Object):
    """Attributes:
        ID: ``0xe4def5db``

    Args:
        peer: Either :obj:`PeerUser <pyrogram.api.types.PeerUser>`, :obj:`PeerChat <pyrogram.api.types.PeerChat>` or :obj:`PeerChannel <pyrogram.api.types.PeerChannel>`
        top_message: ``int`` ``32-bit``
        read_inbox_max_id: ``int`` ``32-bit``
        read_outbox_max_id: ``int`` ``32-bit``
        unread_count: ``int`` ``32-bit``
        unread_mentions_count: ``int`` ``32-bit``
        notify_settings: :obj:`PeerNotifySettings <pyrogram.api.types.PeerNotifySettings>`
        pinned (optional): ``bool``
        pts (optional): ``int`` ``32-bit``
        draft (optional): Either :obj:`DraftMessageEmpty <pyrogram.api.types.DraftMessageEmpty>` or :obj:`DraftMessage <pyrogram.api.types.DraftMessage>`
    """

    ID = 0xe4def5db

    def __init__(self, peer, top_message: int, read_inbox_max_id: int, read_outbox_max_id: int, unread_count: int, unread_mentions_count: int, notify_settings, pinned: bool = None, pts: int = None, draft=None):
        self.pinned = pinned  # flags.2?true
        self.peer = peer  # Peer
        self.top_message = top_message  # int
        self.read_inbox_max_id = read_inbox_max_id  # int
        self.read_outbox_max_id = read_outbox_max_id  # int
        self.unread_count = unread_count  # int
        self.unread_mentions_count = unread_mentions_count  # int
        self.notify_settings = notify_settings  # PeerNotifySettings
        self.pts = pts  # flags.0?int
        self.draft = draft  # flags.1?DraftMessage

    @staticmethod
    def read(b: BytesIO, *args) -> "Dialog":
        flags = Int.read(b)
        
        pinned = True if flags & (1 << 2) else False
        peer = Object.read(b)
        
        top_message = Int.read(b)
        
        read_inbox_max_id = Int.read(b)
        
        read_outbox_max_id = Int.read(b)
        
        unread_count = Int.read(b)
        
        unread_mentions_count = Int.read(b)
        
        notify_settings = Object.read(b)
        
        pts = Int.read(b) if flags & (1 << 0) else None
        draft = Object.read(b) if flags & (1 << 1) else None
        
        return Dialog(peer, top_message, read_inbox_max_id, read_outbox_max_id, unread_count, unread_mentions_count, notify_settings, pinned, pts, draft)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.pinned is not None else 0
        flags |= (1 << 0) if self.pts is not None else 0
        flags |= (1 << 1) if self.draft is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        b.write(Int(self.top_message))
        
        b.write(Int(self.read_inbox_max_id))
        
        b.write(Int(self.read_outbox_max_id))
        
        b.write(Int(self.unread_count))
        
        b.write(Int(self.unread_mentions_count))
        
        b.write(self.notify_settings.write())
        
        if self.pts is not None:
            b.write(Int(self.pts))
        
        if self.draft is not None:
            b.write(self.draft.write())
        
        return b.getvalue()

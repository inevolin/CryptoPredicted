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


class TopPeerCategoryPeers(Object):
    """Attributes:
        ID: ``0xfb834291``

    Args:
        category: Either :obj:`TopPeerCategoryBotsPM <pyrogram.api.types.TopPeerCategoryBotsPM>`, :obj:`TopPeerCategoryBotsInline <pyrogram.api.types.TopPeerCategoryBotsInline>`, :obj:`TopPeerCategoryCorrespondents <pyrogram.api.types.TopPeerCategoryCorrespondents>`, :obj:`TopPeerCategoryGroups <pyrogram.api.types.TopPeerCategoryGroups>`, :obj:`TopPeerCategoryChannels <pyrogram.api.types.TopPeerCategoryChannels>` or :obj:`TopPeerCategoryPhoneCalls <pyrogram.api.types.TopPeerCategoryPhoneCalls>`
        count: ``int`` ``32-bit``
        peers: List of :obj:`TopPeer <pyrogram.api.types.TopPeer>`
    """

    ID = 0xfb834291

    def __init__(self, category, count: int, peers: list):
        self.category = category  # TopPeerCategory
        self.count = count  # int
        self.peers = peers  # Vector<TopPeer>

    @staticmethod
    def read(b: BytesIO, *args) -> "TopPeerCategoryPeers":
        # No flags
        
        category = Object.read(b)
        
        count = Int.read(b)
        
        peers = Object.read(b)
        
        return TopPeerCategoryPeers(category, count, peers)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.category.write())
        
        b.write(Int(self.count))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()

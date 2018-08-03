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


class UpdateNotifySettings(Object):
    """Attributes:
        ID: ``0x84be5b93``

    Args:
        peer: Either :obj:`InputNotifyPeer <pyrogram.api.types.InputNotifyPeer>`, :obj:`InputNotifyUsers <pyrogram.api.types.InputNotifyUsers>` or :obj:`InputNotifyChats <pyrogram.api.types.InputNotifyChats>`
        settings: :obj:`InputPeerNotifySettings <pyrogram.api.types.InputPeerNotifySettings>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x84be5b93

    def __init__(self, peer, settings):
        self.peer = peer  # InputNotifyPeer
        self.settings = settings  # InputPeerNotifySettings

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateNotifySettings":
        # No flags
        
        peer = Object.read(b)
        
        settings = Object.read(b)
        
        return UpdateNotifySettings(peer, settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.settings.write())
        
        return b.getvalue()

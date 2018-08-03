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


class ChatInvite(Object):
    """Attributes:
        ID: ``0xdb74f558``

    Args:
        title: ``str``
        photo: Either :obj:`ChatPhotoEmpty <pyrogram.api.types.ChatPhotoEmpty>` or :obj:`ChatPhoto <pyrogram.api.types.ChatPhoto>`
        participants_count: ``int`` ``32-bit``
        channel (optional): ``bool``
        broadcast (optional): ``bool``
        public (optional): ``bool``
        megagroup (optional): ``bool``
        participants (optional): List of either :obj:`UserEmpty <pyrogram.api.types.UserEmpty>` or :obj:`User <pyrogram.api.types.User>`

    See Also:
        This object can be returned by :obj:`messages.CheckChatInvite <pyrogram.api.functions.messages.CheckChatInvite>`.
    """

    ID = 0xdb74f558

    def __init__(self, title: str, photo, participants_count: int, channel: bool = None, broadcast: bool = None, public: bool = None, megagroup: bool = None, participants: list = None):
        self.channel = channel  # flags.0?true
        self.broadcast = broadcast  # flags.1?true
        self.public = public  # flags.2?true
        self.megagroup = megagroup  # flags.3?true
        self.title = title  # string
        self.photo = photo  # ChatPhoto
        self.participants_count = participants_count  # int
        self.participants = participants  # flags.4?Vector<User>

    @staticmethod
    def read(b: BytesIO, *args) -> "ChatInvite":
        flags = Int.read(b)
        
        channel = True if flags & (1 << 0) else False
        broadcast = True if flags & (1 << 1) else False
        public = True if flags & (1 << 2) else False
        megagroup = True if flags & (1 << 3) else False
        title = String.read(b)
        
        photo = Object.read(b)
        
        participants_count = Int.read(b)
        
        participants = Object.read(b) if flags & (1 << 4) else []
        
        return ChatInvite(title, photo, participants_count, channel, broadcast, public, megagroup, participants)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.channel is not None else 0
        flags |= (1 << 1) if self.broadcast is not None else 0
        flags |= (1 << 2) if self.public is not None else 0
        flags |= (1 << 3) if self.megagroup is not None else 0
        flags |= (1 << 4) if self.participants is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.title))
        
        b.write(self.photo.write())
        
        b.write(Int(self.participants_count))
        
        if self.participants is not None:
            b.write(Vector(self.participants))
        
        return b.getvalue()

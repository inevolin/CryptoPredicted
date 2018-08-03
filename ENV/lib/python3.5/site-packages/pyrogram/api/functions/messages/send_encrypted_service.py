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


class SendEncryptedService(Object):
    """Attributes:
        ID: ``0x32d439a4``

    Args:
        peer: :obj:`InputEncryptedChat <pyrogram.api.types.InputEncryptedChat>`
        random_id: ``int`` ``64-bit``
        data: ``bytes``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`messages.SentEncryptedMessage <pyrogram.api.types.messages.SentEncryptedMessage>` or :obj:`messages.SentEncryptedFile <pyrogram.api.types.messages.SentEncryptedFile>`
    """

    ID = 0x32d439a4

    def __init__(self, peer, random_id: int, data: bytes):
        self.peer = peer  # InputEncryptedChat
        self.random_id = random_id  # long
        self.data = data  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SendEncryptedService":
        # No flags
        
        peer = Object.read(b)
        
        random_id = Long.read(b)
        
        data = Bytes.read(b)
        
        return SendEncryptedService(peer, random_id, data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Long(self.random_id))
        
        b.write(Bytes(self.data))
        
        return b.getvalue()

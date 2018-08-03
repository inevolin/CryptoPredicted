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


class UpdateNewEncryptedMessage(Object):
    """Attributes:
        ID: ``0x12bcbd9a``

    Args:
        message: Either :obj:`EncryptedMessage <pyrogram.api.types.EncryptedMessage>` or :obj:`EncryptedMessageService <pyrogram.api.types.EncryptedMessageService>`
        qts: ``int`` ``32-bit``
    """

    ID = 0x12bcbd9a

    def __init__(self, message, qts: int):
        self.message = message  # EncryptedMessage
        self.qts = qts  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateNewEncryptedMessage":
        # No flags
        
        message = Object.read(b)
        
        qts = Int.read(b)
        
        return UpdateNewEncryptedMessage(message, qts)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.message.write())
        
        b.write(Int(self.qts))
        
        return b.getvalue()

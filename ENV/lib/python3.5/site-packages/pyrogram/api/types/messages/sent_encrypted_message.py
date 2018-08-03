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


class SentEncryptedMessage(Object):
    """Attributes:
        ID: ``0x560f8935``

    Args:
        date: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.SendEncrypted <pyrogram.api.functions.messages.SendEncrypted>`, :obj:`messages.SendEncryptedFile <pyrogram.api.functions.messages.SendEncryptedFile>` and :obj:`messages.SendEncryptedService <pyrogram.api.functions.messages.SendEncryptedService>`.
    """

    ID = 0x560f8935

    def __init__(self, date: int):
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SentEncryptedMessage":
        # No flags
        
        date = Int.read(b)
        
        return SentEncryptedMessage(date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        return b.getvalue()

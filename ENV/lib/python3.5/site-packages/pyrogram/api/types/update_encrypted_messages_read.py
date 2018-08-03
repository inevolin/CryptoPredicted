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


class UpdateEncryptedMessagesRead(Object):
    """Attributes:
        ID: ``0x38fe25b7``

    Args:
        chat_id: ``int`` ``32-bit``
        max_date: ``int`` ``32-bit``
        date: ``int`` ``32-bit``
    """

    ID = 0x38fe25b7

    def __init__(self, chat_id: int, max_date: int, date: int):
        self.chat_id = chat_id  # int
        self.max_date = max_date  # int
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateEncryptedMessagesRead":
        # No flags
        
        chat_id = Int.read(b)
        
        max_date = Int.read(b)
        
        date = Int.read(b)
        
        return UpdateEncryptedMessagesRead(chat_id, max_date, date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.chat_id))
        
        b.write(Int(self.max_date))
        
        b.write(Int(self.date))
        
        return b.getvalue()

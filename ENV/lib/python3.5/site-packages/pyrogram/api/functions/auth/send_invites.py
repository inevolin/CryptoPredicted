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


class SendInvites(Object):
    """Attributes:
        ID: ``0x771c1d97``

    Args:
        phone_numbers: List of ``str``
        message: ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x771c1d97

    def __init__(self, phone_numbers: list, message: str):
        self.phone_numbers = phone_numbers  # Vector<string>
        self.message = message  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "SendInvites":
        # No flags
        
        phone_numbers = Object.read(b, String)
        
        message = String.read(b)
        
        return SendInvites(phone_numbers, message)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.phone_numbers, String))
        
        b.write(String(self.message))
        
        return b.getvalue()

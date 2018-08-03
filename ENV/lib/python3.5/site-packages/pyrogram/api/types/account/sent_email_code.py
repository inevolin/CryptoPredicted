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


class SentEmailCode(Object):
    """Attributes:
        ID: ``0x811f854f``

    Args:
        email_pattern: ``str``
        length: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`account.SendVerifyEmailCode <pyrogram.api.functions.account.SendVerifyEmailCode>`.
    """

    ID = 0x811f854f

    def __init__(self, email_pattern: str, length: int):
        self.email_pattern = email_pattern  # string
        self.length = length  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "SentEmailCode":
        # No flags
        
        email_pattern = String.read(b)
        
        length = Int.read(b)
        
        return SentEmailCode(email_pattern, length)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.email_pattern))
        
        b.write(Int(self.length))
        
        return b.getvalue()

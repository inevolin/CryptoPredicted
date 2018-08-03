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


class GetTmpPassword(Object):
    """Attributes:
        ID: ``0x4a82327e``

    Args:
        password_hash: ``bytes``
        period: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`account.TmpPassword <pyrogram.api.types.account.TmpPassword>`
    """

    ID = 0x4a82327e

    def __init__(self, password_hash: bytes, period: int):
        self.password_hash = password_hash  # bytes
        self.period = period  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetTmpPassword":
        # No flags
        
        password_hash = Bytes.read(b)
        
        period = Int.read(b)
        
        return GetTmpPassword(password_hash, period)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.password_hash))
        
        b.write(Int(self.period))
        
        return b.getvalue()

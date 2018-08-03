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


class UnregisterDevice(Object):
    """Attributes:
        ID: ``0x3076c4bf``

    Args:
        token_type: ``int`` ``32-bit``
        token: ``str``
        other_uids: List of ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0x3076c4bf

    def __init__(self, token_type: int, token: str, other_uids: list):
        self.token_type = token_type  # int
        self.token = token  # string
        self.other_uids = other_uids  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args) -> "UnregisterDevice":
        # No flags
        
        token_type = Int.read(b)
        
        token = String.read(b)
        
        other_uids = Object.read(b, Int)
        
        return UnregisterDevice(token_type, token, other_uids)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.token_type))
        
        b.write(String(self.token))
        
        b.write(Vector(self.other_uids, Int))
        
        return b.getvalue()

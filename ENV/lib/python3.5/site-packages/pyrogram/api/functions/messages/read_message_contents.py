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


class ReadMessageContents(Object):
    """Attributes:
        ID: ``0x36a73f77``

    Args:
        id: List of ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`messages.AffectedMessages <pyrogram.api.types.messages.AffectedMessages>`
    """

    ID = 0x36a73f77

    def __init__(self, id: list):
        self.id = id  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args) -> "ReadMessageContents":
        # No flags
        
        id = Object.read(b, Int)
        
        return ReadMessageContents(id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id, Int))
        
        return b.getvalue()

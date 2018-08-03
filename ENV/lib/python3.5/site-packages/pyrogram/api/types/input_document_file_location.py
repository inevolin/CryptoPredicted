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


class InputDocumentFileLocation(Object):
    """Attributes:
        ID: ``0x430f0724``

    Args:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        version: ``int`` ``32-bit``
    """

    ID = 0x430f0724

    def __init__(self, id: int, access_hash: int, version: int):
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.version = version  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "InputDocumentFileLocation":
        # No flags
        
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        version = Int.read(b)
        
        return InputDocumentFileLocation(id, access_hash, version)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(Int(self.version))
        
        return b.getvalue()

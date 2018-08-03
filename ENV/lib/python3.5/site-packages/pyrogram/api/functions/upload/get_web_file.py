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


class GetWebFile(Object):
    """Attributes:
        ID: ``0x24e6818d``

    Args:
        location: Either :obj:`InputWebFileLocation <pyrogram.api.types.InputWebFileLocation>`, :obj:`InputWebFileGeoPointLocation <pyrogram.api.types.InputWebFileGeoPointLocation>` or :obj:`InputWebFileGeoMessageLocation <pyrogram.api.types.InputWebFileGeoMessageLocation>`
        offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`upload.WebFile <pyrogram.api.types.upload.WebFile>`
    """

    ID = 0x24e6818d

    def __init__(self, location, offset: int, limit: int):
        self.location = location  # InputWebFileLocation
        self.offset = offset  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetWebFile":
        # No flags
        
        location = Object.read(b)
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        return GetWebFile(location, offset, limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.location.write())
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

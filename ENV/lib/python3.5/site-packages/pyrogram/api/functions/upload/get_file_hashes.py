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


class GetFileHashes(Object):
    """Attributes:
        ID: ``0xc7025931``

    Args:
        location: Either :obj:`InputFileLocation <pyrogram.api.types.InputFileLocation>`, :obj:`InputEncryptedFileLocation <pyrogram.api.types.InputEncryptedFileLocation>`, :obj:`InputDocumentFileLocation <pyrogram.api.types.InputDocumentFileLocation>` or :obj:`InputSecureFileLocation <pyrogram.api.types.InputSecureFileLocation>`
        offset: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        List of :obj:`FileHash <pyrogram.api.types.FileHash>`
    """

    ID = 0xc7025931

    def __init__(self, location, offset: int):
        self.location = location  # InputFileLocation
        self.offset = offset  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetFileHashes":
        # No flags
        
        location = Object.read(b)
        
        offset = Int.read(b)
        
        return GetFileHashes(location, offset)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.location.write())
        
        b.write(Int(self.offset))
        
        return b.getvalue()

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


class GetFile(Object):
    """Attributes:
        ID: ``0xe3a6cfb5``

    Args:
        location: Either :obj:`InputFileLocation <pyrogram.api.types.InputFileLocation>`, :obj:`InputEncryptedFileLocation <pyrogram.api.types.InputEncryptedFileLocation>`, :obj:`InputDocumentFileLocation <pyrogram.api.types.InputDocumentFileLocation>` or :obj:`InputSecureFileLocation <pyrogram.api.types.InputSecureFileLocation>`
        offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        Either :obj:`upload.File <pyrogram.api.types.upload.File>` or :obj:`upload.FileCdnRedirect <pyrogram.api.types.upload.FileCdnRedirect>`
    """

    ID = 0xe3a6cfb5

    def __init__(self, location, offset: int, limit: int):
        self.location = location  # InputFileLocation
        self.offset = offset  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "GetFile":
        # No flags
        
        location = Object.read(b)
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        return GetFile(location, offset, limit)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.location.write())
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()

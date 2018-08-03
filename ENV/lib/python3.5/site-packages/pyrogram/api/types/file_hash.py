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


class FileHash(Object):
    """Attributes:
        ID: ``0x6242c773``

    Args:
        offset: ``int`` ``32-bit``
        limit: ``int`` ``32-bit``
        hash: ``bytes``

    See Also:
        This object can be returned by :obj:`upload.ReuploadCdnFile <pyrogram.api.functions.upload.ReuploadCdnFile>`, :obj:`upload.GetCdnFileHashes <pyrogram.api.functions.upload.GetCdnFileHashes>` and :obj:`upload.GetFileHashes <pyrogram.api.functions.upload.GetFileHashes>`.
    """

    ID = 0x6242c773

    def __init__(self, offset: int, limit: int, hash: bytes):
        self.offset = offset  # int
        self.limit = limit  # int
        self.hash = hash  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "FileHash":
        # No flags
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        hash = Bytes.read(b)
        
        return FileHash(offset, limit, hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        b.write(Bytes(self.hash))
        
        return b.getvalue()

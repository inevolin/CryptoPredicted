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


class File(Object):
    """Attributes:
        ID: ``0x096a18d5``

    Args:
        type: Either :obj:`storage.FileUnknown <pyrogram.api.types.storage.FileUnknown>`, :obj:`storage.FilePartial <pyrogram.api.types.storage.FilePartial>`, :obj:`storage.FileJpeg <pyrogram.api.types.storage.FileJpeg>`, :obj:`storage.FileGif <pyrogram.api.types.storage.FileGif>`, :obj:`storage.FilePng <pyrogram.api.types.storage.FilePng>`, :obj:`storage.FilePdf <pyrogram.api.types.storage.FilePdf>`, :obj:`storage.FileMp3 <pyrogram.api.types.storage.FileMp3>`, :obj:`storage.FileMov <pyrogram.api.types.storage.FileMov>`, :obj:`storage.FileMp4 <pyrogram.api.types.storage.FileMp4>` or :obj:`storage.FileWebp <pyrogram.api.types.storage.FileWebp>`
        mtime: ``int`` ``32-bit``
        bytes: ``bytes``

    See Also:
        This object can be returned by :obj:`upload.GetFile <pyrogram.api.functions.upload.GetFile>`.
    """

    ID = 0x096a18d5

    def __init__(self, type, mtime: int, bytes: bytes):
        self.type = type  # storage.FileType
        self.mtime = mtime  # int
        self.bytes = bytes  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "File":
        # No flags
        
        type = Object.read(b)
        
        mtime = Int.read(b)
        
        bytes = Bytes.read(b)
        
        return File(type, mtime, bytes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Int(self.mtime))
        
        b.write(Bytes(self.bytes))
        
        return b.getvalue()

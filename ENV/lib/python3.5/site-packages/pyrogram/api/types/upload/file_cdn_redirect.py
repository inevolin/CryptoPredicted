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


class FileCdnRedirect(Object):
    """Attributes:
        ID: ``0xf18cda44``

    Args:
        dc_id: ``int`` ``32-bit``
        file_token: ``bytes``
        encryption_key: ``bytes``
        encryption_iv: ``bytes``
        file_hashes: List of :obj:`FileHash <pyrogram.api.types.FileHash>`

    See Also:
        This object can be returned by :obj:`upload.GetFile <pyrogram.api.functions.upload.GetFile>`.
    """

    ID = 0xf18cda44

    def __init__(self, dc_id: int, file_token: bytes, encryption_key: bytes, encryption_iv: bytes, file_hashes: list):
        self.dc_id = dc_id  # int
        self.file_token = file_token  # bytes
        self.encryption_key = encryption_key  # bytes
        self.encryption_iv = encryption_iv  # bytes
        self.file_hashes = file_hashes  # Vector<FileHash>

    @staticmethod
    def read(b: BytesIO, *args) -> "FileCdnRedirect":
        # No flags
        
        dc_id = Int.read(b)
        
        file_token = Bytes.read(b)
        
        encryption_key = Bytes.read(b)
        
        encryption_iv = Bytes.read(b)
        
        file_hashes = Object.read(b)
        
        return FileCdnRedirect(dc_id, file_token, encryption_key, encryption_iv, file_hashes)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.dc_id))
        
        b.write(Bytes(self.file_token))
        
        b.write(Bytes(self.encryption_key))
        
        b.write(Bytes(self.encryption_iv))
        
        b.write(Vector(self.file_hashes))
        
        return b.getvalue()

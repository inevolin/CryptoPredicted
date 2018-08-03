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


class EncryptedFile(Object):
    """Attributes:
        ID: ``0x4a70994c``

    Args:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        size: ``int`` ``32-bit``
        dc_id: ``int`` ``32-bit``
        key_fingerprint: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`messages.UploadEncryptedFile <pyrogram.api.functions.messages.UploadEncryptedFile>`.
    """

    ID = 0x4a70994c

    def __init__(self, id: int, access_hash: int, size: int, dc_id: int, key_fingerprint: int):
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.size = size  # int
        self.dc_id = dc_id  # int
        self.key_fingerprint = key_fingerprint  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "EncryptedFile":
        # No flags
        
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        size = Int.read(b)
        
        dc_id = Int.read(b)
        
        key_fingerprint = Int.read(b)
        
        return EncryptedFile(id, access_hash, size, dc_id, key_fingerprint)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(Int(self.size))
        
        b.write(Int(self.dc_id))
        
        b.write(Int(self.key_fingerprint))
        
        return b.getvalue()

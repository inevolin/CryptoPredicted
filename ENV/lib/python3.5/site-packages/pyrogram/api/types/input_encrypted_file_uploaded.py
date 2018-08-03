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


class InputEncryptedFileUploaded(Object):
    """Attributes:
        ID: ``0x64bd0306``

    Args:
        id: ``int`` ``64-bit``
        parts: ``int`` ``32-bit``
        md5_checksum: ``str``
        key_fingerprint: ``int`` ``32-bit``
    """

    ID = 0x64bd0306

    def __init__(self, id: int, parts: int, md5_checksum: str, key_fingerprint: int):
        self.id = id  # long
        self.parts = parts  # int
        self.md5_checksum = md5_checksum  # string
        self.key_fingerprint = key_fingerprint  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "InputEncryptedFileUploaded":
        # No flags
        
        id = Long.read(b)
        
        parts = Int.read(b)
        
        md5_checksum = String.read(b)
        
        key_fingerprint = Int.read(b)
        
        return InputEncryptedFileUploaded(id, parts, md5_checksum, key_fingerprint)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Int(self.parts))
        
        b.write(String(self.md5_checksum))
        
        b.write(Int(self.key_fingerprint))
        
        return b.getvalue()

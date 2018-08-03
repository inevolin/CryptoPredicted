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


class SecureCredentialsEncrypted(Object):
    """Attributes:
        ID: ``0x33f0ea47``

    Args:
        data: ``bytes``
        hash: ``bytes``
        secret: ``bytes``
    """

    ID = 0x33f0ea47

    def __init__(self, data: bytes, hash: bytes, secret: bytes):
        self.data = data  # bytes
        self.hash = hash  # bytes
        self.secret = secret  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "SecureCredentialsEncrypted":
        # No flags
        
        data = Bytes.read(b)
        
        hash = Bytes.read(b)
        
        secret = Bytes.read(b)
        
        return SecureCredentialsEncrypted(data, hash, secret)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.data))
        
        b.write(Bytes(self.hash))
        
        b.write(Bytes(self.secret))
        
        return b.getvalue()

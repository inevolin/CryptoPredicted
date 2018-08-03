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


class MessageActionSecureValuesSentMe(Object):
    """Attributes:
        ID: ``0x1b287353``

    Args:
        values: List of :obj:`SecureValue <pyrogram.api.types.SecureValue>`
        credentials: :obj:`SecureCredentialsEncrypted <pyrogram.api.types.SecureCredentialsEncrypted>`
    """

    ID = 0x1b287353

    def __init__(self, values: list, credentials):
        self.values = values  # Vector<SecureValue>
        self.credentials = credentials  # SecureCredentialsEncrypted

    @staticmethod
    def read(b: BytesIO, *args) -> "MessageActionSecureValuesSentMe":
        # No flags
        
        values = Object.read(b)
        
        credentials = Object.read(b)
        
        return MessageActionSecureValuesSentMe(values, credentials)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.values))
        
        b.write(self.credentials.write())
        
        return b.getvalue()

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


class AcceptAuthorization(Object):
    """Attributes:
        ID: ``0xe7027c94``

    Args:
        bot_id: ``int`` ``32-bit``
        scope: ``str``
        public_key: ``str``
        value_hashes: List of :obj:`SecureValueHash <pyrogram.api.types.SecureValueHash>`
        credentials: :obj:`SecureCredentialsEncrypted <pyrogram.api.types.SecureCredentialsEncrypted>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xe7027c94

    def __init__(self, bot_id: int, scope: str, public_key: str, value_hashes: list, credentials):
        self.bot_id = bot_id  # int
        self.scope = scope  # string
        self.public_key = public_key  # string
        self.value_hashes = value_hashes  # Vector<SecureValueHash>
        self.credentials = credentials  # SecureCredentialsEncrypted

    @staticmethod
    def read(b: BytesIO, *args) -> "AcceptAuthorization":
        # No flags
        
        bot_id = Int.read(b)
        
        scope = String.read(b)
        
        public_key = String.read(b)
        
        value_hashes = Object.read(b)
        
        credentials = Object.read(b)
        
        return AcceptAuthorization(bot_id, scope, public_key, value_hashes, credentials)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.bot_id))
        
        b.write(String(self.scope))
        
        b.write(String(self.public_key))
        
        b.write(Vector(self.value_hashes))
        
        b.write(self.credentials.write())
        
        return b.getvalue()

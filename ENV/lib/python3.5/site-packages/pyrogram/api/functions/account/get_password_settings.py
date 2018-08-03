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


class GetPasswordSettings(Object):
    """Attributes:
        ID: ``0xbc8d11bb``

    Args:
        current_password_hash: ``bytes``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`account.PasswordSettings <pyrogram.api.types.account.PasswordSettings>`
    """

    ID = 0xbc8d11bb

    def __init__(self, current_password_hash: bytes):
        self.current_password_hash = current_password_hash  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "GetPasswordSettings":
        # No flags
        
        current_password_hash = Bytes.read(b)
        
        return GetPasswordSettings(current_password_hash)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.current_password_hash))
        
        return b.getvalue()

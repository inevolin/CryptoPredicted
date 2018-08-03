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


class PasswordSettings(Object):
    """Attributes:
        ID: ``0x7bd9c3f1``

    Args:
        email: ``str``
        secure_salt: ``bytes``
        secure_secret: ``bytes``
        secure_secret_id: ``int`` ``64-bit``

    See Also:
        This object can be returned by :obj:`account.GetPasswordSettings <pyrogram.api.functions.account.GetPasswordSettings>`.
    """

    ID = 0x7bd9c3f1

    def __init__(self, email: str, secure_salt: bytes, secure_secret: bytes, secure_secret_id: int):
        self.email = email  # string
        self.secure_salt = secure_salt  # bytes
        self.secure_secret = secure_secret  # bytes
        self.secure_secret_id = secure_secret_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "PasswordSettings":
        # No flags
        
        email = String.read(b)
        
        secure_salt = Bytes.read(b)
        
        secure_secret = Bytes.read(b)
        
        secure_secret_id = Long.read(b)
        
        return PasswordSettings(email, secure_salt, secure_secret, secure_secret_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.email))
        
        b.write(Bytes(self.secure_salt))
        
        b.write(Bytes(self.secure_secret))
        
        b.write(Long(self.secure_secret_id))
        
        return b.getvalue()

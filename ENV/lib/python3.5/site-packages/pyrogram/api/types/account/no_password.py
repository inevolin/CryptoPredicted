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


class NoPassword(Object):
    """Attributes:
        ID: ``0x5ea182f6``

    Args:
        new_salt: ``bytes``
        new_secure_salt: ``bytes``
        secure_random: ``bytes``
        email_unconfirmed_pattern: ``str``

    See Also:
        This object can be returned by :obj:`account.GetPassword <pyrogram.api.functions.account.GetPassword>`.
    """

    ID = 0x5ea182f6

    def __init__(self, new_salt: bytes, new_secure_salt: bytes, secure_random: bytes, email_unconfirmed_pattern: str):
        self.new_salt = new_salt  # bytes
        self.new_secure_salt = new_secure_salt  # bytes
        self.secure_random = secure_random  # bytes
        self.email_unconfirmed_pattern = email_unconfirmed_pattern  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "NoPassword":
        # No flags
        
        new_salt = Bytes.read(b)
        
        new_secure_salt = Bytes.read(b)
        
        secure_random = Bytes.read(b)
        
        email_unconfirmed_pattern = String.read(b)
        
        return NoPassword(new_salt, new_secure_salt, secure_random, email_unconfirmed_pattern)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.new_salt))
        
        b.write(Bytes(self.new_secure_salt))
        
        b.write(Bytes(self.secure_random))
        
        b.write(String(self.email_unconfirmed_pattern))
        
        return b.getvalue()

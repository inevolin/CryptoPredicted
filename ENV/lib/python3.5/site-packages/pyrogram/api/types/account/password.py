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


class Password(Object):
    """Attributes:
        ID: ``0xca39b447``

    Args:
        current_salt: ``bytes``
        new_salt: ``bytes``
        new_secure_salt: ``bytes``
        secure_random: ``bytes``
        hint: ``str``
        email_unconfirmed_pattern: ``str``
        has_recovery (optional): ``bool``
        has_secure_values (optional): ``bool``

    See Also:
        This object can be returned by :obj:`account.GetPassword <pyrogram.api.functions.account.GetPassword>`.
    """

    ID = 0xca39b447

    def __init__(self, current_salt: bytes, new_salt: bytes, new_secure_salt: bytes, secure_random: bytes, hint: str, email_unconfirmed_pattern: str, has_recovery: bool = None, has_secure_values: bool = None):
        self.has_recovery = has_recovery  # flags.0?true
        self.has_secure_values = has_secure_values  # flags.1?true
        self.current_salt = current_salt  # bytes
        self.new_salt = new_salt  # bytes
        self.new_secure_salt = new_secure_salt  # bytes
        self.secure_random = secure_random  # bytes
        self.hint = hint  # string
        self.email_unconfirmed_pattern = email_unconfirmed_pattern  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "Password":
        flags = Int.read(b)
        
        has_recovery = True if flags & (1 << 0) else False
        has_secure_values = True if flags & (1 << 1) else False
        current_salt = Bytes.read(b)
        
        new_salt = Bytes.read(b)
        
        new_secure_salt = Bytes.read(b)
        
        secure_random = Bytes.read(b)
        
        hint = String.read(b)
        
        email_unconfirmed_pattern = String.read(b)
        
        return Password(current_salt, new_salt, new_secure_salt, secure_random, hint, email_unconfirmed_pattern, has_recovery, has_secure_values)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.has_recovery is not None else 0
        flags |= (1 << 1) if self.has_secure_values is not None else 0
        b.write(Int(flags))
        
        b.write(Bytes(self.current_salt))
        
        b.write(Bytes(self.new_salt))
        
        b.write(Bytes(self.new_secure_salt))
        
        b.write(Bytes(self.secure_random))
        
        b.write(String(self.hint))
        
        b.write(String(self.email_unconfirmed_pattern))
        
        return b.getvalue()

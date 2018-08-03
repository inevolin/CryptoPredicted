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


class UpdatePasswordSettings(Object):
    """Attributes:
        ID: ``0xfa7c4b86``

    Args:
        current_password_hash: ``bytes``
        new_settings: :obj:`account.PasswordInputSettings <pyrogram.api.types.account.PasswordInputSettings>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        ``bool``
    """

    ID = 0xfa7c4b86

    def __init__(self, current_password_hash: bytes, new_settings):
        self.current_password_hash = current_password_hash  # bytes
        self.new_settings = new_settings  # account.PasswordInputSettings

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdatePasswordSettings":
        # No flags
        
        current_password_hash = Bytes.read(b)
        
        new_settings = Object.read(b)
        
        return UpdatePasswordSettings(current_password_hash, new_settings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.current_password_hash))
        
        b.write(self.new_settings.write())
        
        return b.getvalue()

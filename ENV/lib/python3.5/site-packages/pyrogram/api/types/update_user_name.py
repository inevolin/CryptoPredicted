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


class UpdateUserName(Object):
    """Attributes:
        ID: ``0xa7332b73``

    Args:
        user_id: ``int`` ``32-bit``
        first_name: ``str``
        last_name: ``str``
        username: ``str``
    """

    ID = 0xa7332b73

    def __init__(self, user_id: int, first_name: str, last_name: str, username: str):
        self.user_id = user_id  # int
        self.first_name = first_name  # string
        self.last_name = last_name  # string
        self.username = username  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "UpdateUserName":
        # No flags
        
        user_id = Int.read(b)
        
        first_name = String.read(b)
        
        last_name = String.read(b)
        
        username = String.read(b)
        
        return UpdateUserName(user_id, first_name, last_name, username)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.user_id))
        
        b.write(String(self.first_name))
        
        b.write(String(self.last_name))
        
        b.write(String(self.username))
        
        return b.getvalue()

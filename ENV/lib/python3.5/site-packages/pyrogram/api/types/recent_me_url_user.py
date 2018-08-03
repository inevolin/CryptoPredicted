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


class RecentMeUrlUser(Object):
    """Attributes:
        ID: ``0x8dbc3336``

    Args:
        url: ``str``
        user_id: ``int`` ``32-bit``
    """

    ID = 0x8dbc3336

    def __init__(self, url: str, user_id: int):
        self.url = url  # string
        self.user_id = user_id  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "RecentMeUrlUser":
        # No flags
        
        url = String.read(b)
        
        user_id = Int.read(b)
        
        return RecentMeUrlUser(url, user_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        b.write(Int(self.user_id))
        
        return b.getvalue()

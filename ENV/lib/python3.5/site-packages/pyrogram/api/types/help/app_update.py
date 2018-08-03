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


class AppUpdate(Object):
    """Attributes:
        ID: ``0x8987f311``

    Args:
        id: ``int`` ``32-bit``
        critical: ``bool``
        url: ``str``
        text: ``str``

    See Also:
        This object can be returned by :obj:`help.GetAppUpdate <pyrogram.api.functions.help.GetAppUpdate>`.
    """

    ID = 0x8987f311

    def __init__(self, id: int, critical: bool, url: str, text: str):
        self.id = id  # int
        self.critical = critical  # Bool
        self.url = url  # string
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "AppUpdate":
        # No flags
        
        id = Int.read(b)
        
        critical = Bool.read(b)
        
        url = String.read(b)
        
        text = String.read(b)
        
        return AppUpdate(id, critical, url, text)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Bool(self.critical))
        
        b.write(String(self.url))
        
        b.write(String(self.text))
        
        return b.getvalue()

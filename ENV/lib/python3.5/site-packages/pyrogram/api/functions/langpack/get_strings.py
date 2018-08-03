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


class GetStrings(Object):
    """Attributes:
        ID: ``0x2e1ee318``

    Args:
        lang_code: ``str``
        keys: List of ``str``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        List of either :obj:`LangPackString <pyrogram.api.types.LangPackString>`, :obj:`LangPackStringPluralized <pyrogram.api.types.LangPackStringPluralized>` or :obj:`LangPackStringDeleted <pyrogram.api.types.LangPackStringDeleted>`
    """

    ID = 0x2e1ee318

    def __init__(self, lang_code: str, keys: list):
        self.lang_code = lang_code  # string
        self.keys = keys  # Vector<string>

    @staticmethod
    def read(b: BytesIO, *args) -> "GetStrings":
        # No flags
        
        lang_code = String.read(b)
        
        keys = Object.read(b, String)
        
        return GetStrings(lang_code, keys)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_code))
        
        b.write(Vector(self.keys, String))
        
        return b.getvalue()

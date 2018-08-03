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


class LangPackString(Object):
    """Attributes:
        ID: ``0xcad181f6``

    Args:
        key: ``str``
        value: ``str``

    See Also:
        This object can be returned by :obj:`langpack.GetStrings <pyrogram.api.functions.langpack.GetStrings>`.
    """

    ID = 0xcad181f6

    def __init__(self, key: str, value: str):
        self.key = key  # string
        self.value = value  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "LangPackString":
        # No flags
        
        key = String.read(b)
        
        value = String.read(b)
        
        return LangPackString(key, value)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.key))
        
        b.write(String(self.value))
        
        return b.getvalue()

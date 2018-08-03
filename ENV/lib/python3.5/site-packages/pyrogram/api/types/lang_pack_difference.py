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


class LangPackDifference(Object):
    """Attributes:
        ID: ``0xf385c1f6``

    Args:
        lang_code: ``str``
        from_version: ``int`` ``32-bit``
        version: ``int`` ``32-bit``
        strings: List of either :obj:`LangPackString <pyrogram.api.types.LangPackString>`, :obj:`LangPackStringPluralized <pyrogram.api.types.LangPackStringPluralized>` or :obj:`LangPackStringDeleted <pyrogram.api.types.LangPackStringDeleted>`

    See Also:
        This object can be returned by :obj:`langpack.GetLangPack <pyrogram.api.functions.langpack.GetLangPack>` and :obj:`langpack.GetDifference <pyrogram.api.functions.langpack.GetDifference>`.
    """

    ID = 0xf385c1f6

    def __init__(self, lang_code: str, from_version: int, version: int, strings: list):
        self.lang_code = lang_code  # string
        self.from_version = from_version  # int
        self.version = version  # int
        self.strings = strings  # Vector<LangPackString>

    @staticmethod
    def read(b: BytesIO, *args) -> "LangPackDifference":
        # No flags
        
        lang_code = String.read(b)
        
        from_version = Int.read(b)
        
        version = Int.read(b)
        
        strings = Object.read(b)
        
        return LangPackDifference(lang_code, from_version, version, strings)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.lang_code))
        
        b.write(Int(self.from_version))
        
        b.write(Int(self.version))
        
        b.write(Vector(self.strings))
        
        return b.getvalue()

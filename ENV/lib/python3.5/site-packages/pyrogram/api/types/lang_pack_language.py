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


class LangPackLanguage(Object):
    """Attributes:
        ID: ``0x117698f1``

    Args:
        name: ``str``
        native_name: ``str``
        lang_code: ``str``

    See Also:
        This object can be returned by :obj:`langpack.GetLanguages <pyrogram.api.functions.langpack.GetLanguages>`.
    """

    ID = 0x117698f1

    def __init__(self, name: str, native_name: str, lang_code: str):
        self.name = name  # string
        self.native_name = native_name  # string
        self.lang_code = lang_code  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "LangPackLanguage":
        # No flags
        
        name = String.read(b)
        
        native_name = String.read(b)
        
        lang_code = String.read(b)
        
        return LangPackLanguage(name, native_name, lang_code)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.name))
        
        b.write(String(self.native_name))
        
        b.write(String(self.lang_code))
        
        return b.getvalue()

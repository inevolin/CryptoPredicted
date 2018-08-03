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


class LangPackStringPluralized(Object):
    """Attributes:
        ID: ``0x6c47ac9f``

    Args:
        key: ``str``
        other_value: ``str``
        zero_value (optional): ``str``
        one_value (optional): ``str``
        two_value (optional): ``str``
        few_value (optional): ``str``
        many_value (optional): ``str``

    See Also:
        This object can be returned by :obj:`langpack.GetStrings <pyrogram.api.functions.langpack.GetStrings>`.
    """

    ID = 0x6c47ac9f

    def __init__(self, key: str, other_value: str, zero_value: str = None, one_value: str = None, two_value: str = None, few_value: str = None, many_value: str = None):
        self.key = key  # string
        self.zero_value = zero_value  # flags.0?string
        self.one_value = one_value  # flags.1?string
        self.two_value = two_value  # flags.2?string
        self.few_value = few_value  # flags.3?string
        self.many_value = many_value  # flags.4?string
        self.other_value = other_value  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "LangPackStringPluralized":
        flags = Int.read(b)
        
        key = String.read(b)
        
        zero_value = String.read(b) if flags & (1 << 0) else None
        one_value = String.read(b) if flags & (1 << 1) else None
        two_value = String.read(b) if flags & (1 << 2) else None
        few_value = String.read(b) if flags & (1 << 3) else None
        many_value = String.read(b) if flags & (1 << 4) else None
        other_value = String.read(b)
        
        return LangPackStringPluralized(key, other_value, zero_value, one_value, two_value, few_value, many_value)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.zero_value is not None else 0
        flags |= (1 << 1) if self.one_value is not None else 0
        flags |= (1 << 2) if self.two_value is not None else 0
        flags |= (1 << 3) if self.few_value is not None else 0
        flags |= (1 << 4) if self.many_value is not None else 0
        b.write(Int(flags))
        
        b.write(String(self.key))
        
        if self.zero_value is not None:
            b.write(String(self.zero_value))
        
        if self.one_value is not None:
            b.write(String(self.one_value))
        
        if self.two_value is not None:
            b.write(String(self.two_value))
        
        if self.few_value is not None:
            b.write(String(self.few_value))
        
        if self.many_value is not None:
            b.write(String(self.many_value))
        
        b.write(String(self.other_value))
        
        return b.getvalue()

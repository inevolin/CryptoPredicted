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


class ConfigSimple(Object):
    """Attributes:
        ID: ``0x5a592a6c``

    Args:
        date: ``int`` ``32-bit``
        expires: ``int`` ``32-bit``
        rules: :obj:`vector<AccessPointRule> <pyrogram.api.types.vector<AccessPointRule>>`
    """

    ID = 0x5a592a6c

    def __init__(self, date: int, expires: int, rules):
        self.date = date  # int
        self.expires = expires  # int
        self.rules = rules  # vector<AccessPointRule>

    @staticmethod
    def read(b: BytesIO, *args) -> "ConfigSimple":
        # No flags
        
        date = Int.read(b)
        
        expires = Int.read(b)
        
        rules = Object.read(b)
        
        return ConfigSimple(date, expires, rules)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        b.write(Int(self.expires))
        
        b.write(Vector(self.rules))
        
        return b.getvalue()

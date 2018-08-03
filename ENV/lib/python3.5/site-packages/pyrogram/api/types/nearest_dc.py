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


class NearestDc(Object):
    """Attributes:
        ID: ``0x8e1a1775``

    Args:
        country: ``str``
        this_dc: ``int`` ``32-bit``
        nearest_dc: ``int`` ``32-bit``

    See Also:
        This object can be returned by :obj:`help.GetNearestDc <pyrogram.api.functions.help.GetNearestDc>`.
    """

    ID = 0x8e1a1775

    def __init__(self, country: str, this_dc: int, nearest_dc: int):
        self.country = country  # string
        self.this_dc = this_dc  # int
        self.nearest_dc = nearest_dc  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "NearestDc":
        # No flags
        
        country = String.read(b)
        
        this_dc = Int.read(b)
        
        nearest_dc = Int.read(b)
        
        return NearestDc(country, this_dc, nearest_dc)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.country))
        
        b.write(Int(self.this_dc))
        
        b.write(Int(self.nearest_dc))
        
        return b.getvalue()

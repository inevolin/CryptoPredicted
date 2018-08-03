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


class GeoPoint(Object):
    """Attributes:
        ID: ``0x2049d70c``

    Args:
        long: ``float`` ``64-bit``
        lat: ``float`` ``64-bit``
    """

    ID = 0x2049d70c

    def __init__(self, long: float, lat: float):
        self.long = long  # double
        self.lat = lat  # double

    @staticmethod
    def read(b: BytesIO, *args) -> "GeoPoint":
        # No flags
        
        long = Double.read(b)
        
        lat = Double.read(b)
        
        return GeoPoint(long, lat)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Double(self.long))
        
        b.write(Double(self.lat))
        
        return b.getvalue()

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


class InputMediaGeoLive(Object):
    """Attributes:
        ID: ``0x7b1a118f``

    Args:
        geo_point: Either :obj:`InputGeoPointEmpty <pyrogram.api.types.InputGeoPointEmpty>` or :obj:`InputGeoPoint <pyrogram.api.types.InputGeoPoint>`
        period: ``int`` ``32-bit``
    """

    ID = 0x7b1a118f

    def __init__(self, geo_point, period: int):
        self.geo_point = geo_point  # InputGeoPoint
        self.period = period  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "InputMediaGeoLive":
        # No flags
        
        geo_point = Object.read(b)
        
        period = Int.read(b)
        
        return InputMediaGeoLive(geo_point, period)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.geo_point.write())
        
        b.write(Int(self.period))
        
        return b.getvalue()

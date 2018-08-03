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


class DataJSON(Object):
    """Attributes:
        ID: ``0x7d748d04``

    Args:
        data: ``str``

    See Also:
        This object can be returned by :obj:`bots.SendCustomRequest <pyrogram.api.functions.bots.SendCustomRequest>` and :obj:`phone.GetCallConfig <pyrogram.api.functions.phone.GetCallConfig>`.
    """

    ID = 0x7d748d04

    def __init__(self, data: str):
        self.data = data  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "DataJSON":
        # No flags
        
        data = String.read(b)
        
        return DataJSON(data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.data))
        
        return b.getvalue()

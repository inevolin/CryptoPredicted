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


class InputClientProxy(Object):
    """Attributes:
        ID: ``0x75588b3f``

    Args:
        address: ``str``
        port: ``int`` ``32-bit``
    """

    ID = 0x75588b3f

    def __init__(self, address: str, port: int):
        self.address = address  # string
        self.port = port  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "InputClientProxy":
        # No flags
        
        address = String.read(b)
        
        port = Int.read(b)
        
        return InputClientProxy(address, port)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.address))
        
        b.write(Int(self.port))
        
        return b.getvalue()

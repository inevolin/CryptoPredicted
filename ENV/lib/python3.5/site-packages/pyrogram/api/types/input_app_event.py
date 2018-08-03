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


class InputAppEvent(Object):
    """Attributes:
        ID: ``0x770656a8``

    Args:
        time: ``float`` ``64-bit``
        type: ``str``
        peer: ``int`` ``64-bit``
        data: ``str``
    """

    ID = 0x770656a8

    def __init__(self, time: float, type: str, peer: int, data: str):
        self.time = time  # double
        self.type = type  # string
        self.peer = peer  # long
        self.data = data  # string

    @staticmethod
    def read(b: BytesIO, *args) -> "InputAppEvent":
        # No flags
        
        time = Double.read(b)
        
        type = String.read(b)
        
        peer = Long.read(b)
        
        data = String.read(b)
        
        return InputAppEvent(time, type, peer, data)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Double(self.time))
        
        b.write(String(self.type))
        
        b.write(Long(self.peer))
        
        b.write(String(self.data))
        
        return b.getvalue()

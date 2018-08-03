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


class IpPortSecret(Object):
    """Attributes:
        ID: ``0x37982646``

    Args:
        ipv4: ``int`` ``32-bit``
        port: ``int`` ``32-bit``
        secret: ``bytes``
    """

    ID = 0x37982646

    def __init__(self, ipv4: int, port: int, secret: bytes):
        self.ipv4 = ipv4  # int
        self.port = port  # int
        self.secret = secret  # bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "IpPortSecret":
        # No flags
        
        ipv4 = Int.read(b)
        
        port = Int.read(b)
        
        secret = Bytes.read(b)
        
        return IpPortSecret(ipv4, port, secret)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.ipv4))
        
        b.write(Int(self.port))
        
        b.write(Bytes(self.secret))
        
        return b.getvalue()

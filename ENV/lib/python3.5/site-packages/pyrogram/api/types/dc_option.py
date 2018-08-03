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


class DcOption(Object):
    """Attributes:
        ID: ``0x18b7a10d``

    Args:
        id: ``int`` ``32-bit``
        ip_address: ``str``
        port: ``int`` ``32-bit``
        ipv6 (optional): ``bool``
        media_only (optional): ``bool``
        tcpo_only (optional): ``bool``
        cdn (optional): ``bool``
        static (optional): ``bool``
        secret (optional): ``bytes``
    """

    ID = 0x18b7a10d

    def __init__(self, id: int, ip_address: str, port: int, ipv6: bool = None, media_only: bool = None, tcpo_only: bool = None, cdn: bool = None, static: bool = None, secret: bytes = None):
        self.ipv6 = ipv6  # flags.0?true
        self.media_only = media_only  # flags.1?true
        self.tcpo_only = tcpo_only  # flags.2?true
        self.cdn = cdn  # flags.3?true
        self.static = static  # flags.4?true
        self.id = id  # int
        self.ip_address = ip_address  # string
        self.port = port  # int
        self.secret = secret  # flags.10?bytes

    @staticmethod
    def read(b: BytesIO, *args) -> "DcOption":
        flags = Int.read(b)
        
        ipv6 = True if flags & (1 << 0) else False
        media_only = True if flags & (1 << 1) else False
        tcpo_only = True if flags & (1 << 2) else False
        cdn = True if flags & (1 << 3) else False
        static = True if flags & (1 << 4) else False
        id = Int.read(b)
        
        ip_address = String.read(b)
        
        port = Int.read(b)
        
        secret = Bytes.read(b) if flags & (1 << 10) else None
        return DcOption(id, ip_address, port, ipv6, media_only, tcpo_only, cdn, static, secret)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.ipv6 is not None else 0
        flags |= (1 << 1) if self.media_only is not None else 0
        flags |= (1 << 2) if self.tcpo_only is not None else 0
        flags |= (1 << 3) if self.cdn is not None else 0
        flags |= (1 << 4) if self.static is not None else 0
        flags |= (1 << 10) if self.secret is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.id))
        
        b.write(String(self.ip_address))
        
        b.write(Int(self.port))
        
        if self.secret is not None:
            b.write(Bytes(self.secret))
        
        return b.getvalue()

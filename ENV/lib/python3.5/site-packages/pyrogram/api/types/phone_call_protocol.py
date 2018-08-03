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


class PhoneCallProtocol(Object):
    """Attributes:
        ID: ``0xa2bb35cb``

    Args:
        min_layer: ``int`` ``32-bit``
        max_layer: ``int`` ``32-bit``
        udp_p2p (optional): ``bool``
        udp_reflector (optional): ``bool``
    """

    ID = 0xa2bb35cb

    def __init__(self, min_layer: int, max_layer: int, udp_p2p: bool = None, udp_reflector: bool = None):
        self.udp_p2p = udp_p2p  # flags.0?true
        self.udp_reflector = udp_reflector  # flags.1?true
        self.min_layer = min_layer  # int
        self.max_layer = max_layer  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "PhoneCallProtocol":
        flags = Int.read(b)
        
        udp_p2p = True if flags & (1 << 0) else False
        udp_reflector = True if flags & (1 << 1) else False
        min_layer = Int.read(b)
        
        max_layer = Int.read(b)
        
        return PhoneCallProtocol(min_layer, max_layer, udp_p2p, udp_reflector)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.udp_p2p is not None else 0
        flags |= (1 << 1) if self.udp_reflector is not None else 0
        b.write(Int(flags))
        
        b.write(Int(self.min_layer))
        
        b.write(Int(self.max_layer))
        
        return b.getvalue()

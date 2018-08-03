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


class AcceptCall(Object):
    """Attributes:
        ID: ``0x3bd2b4a0``

    Args:
        peer: :obj:`InputPhoneCall <pyrogram.api.types.InputPhoneCall>`
        g_b: ``bytes``
        protocol: :obj:`PhoneCallProtocol <pyrogram.api.types.PhoneCallProtocol>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`phone.PhoneCall <pyrogram.api.types.phone.PhoneCall>`
    """

    ID = 0x3bd2b4a0

    def __init__(self, peer, g_b: bytes, protocol):
        self.peer = peer  # InputPhoneCall
        self.g_b = g_b  # bytes
        self.protocol = protocol  # PhoneCallProtocol

    @staticmethod
    def read(b: BytesIO, *args) -> "AcceptCall":
        # No flags
        
        peer = Object.read(b)
        
        g_b = Bytes.read(b)
        
        protocol = Object.read(b)
        
        return AcceptCall(peer, g_b, protocol)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bytes(self.g_b))
        
        b.write(self.protocol.write())
        
        return b.getvalue()

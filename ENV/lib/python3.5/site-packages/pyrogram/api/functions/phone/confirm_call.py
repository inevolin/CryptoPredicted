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


class ConfirmCall(Object):
    """Attributes:
        ID: ``0x2efe1722``

    Args:
        peer: :obj:`InputPhoneCall <pyrogram.api.types.InputPhoneCall>`
        g_a: ``bytes``
        key_fingerprint: ``int`` ``64-bit``
        protocol: :obj:`PhoneCallProtocol <pyrogram.api.types.PhoneCallProtocol>`

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`phone.PhoneCall <pyrogram.api.types.phone.PhoneCall>`
    """

    ID = 0x2efe1722

    def __init__(self, peer, g_a: bytes, key_fingerprint: int, protocol):
        self.peer = peer  # InputPhoneCall
        self.g_a = g_a  # bytes
        self.key_fingerprint = key_fingerprint  # long
        self.protocol = protocol  # PhoneCallProtocol

    @staticmethod
    def read(b: BytesIO, *args) -> "ConfirmCall":
        # No flags
        
        peer = Object.read(b)
        
        g_a = Bytes.read(b)
        
        key_fingerprint = Long.read(b)
        
        protocol = Object.read(b)
        
        return ConfirmCall(peer, g_a, key_fingerprint, protocol)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bytes(self.g_a))
        
        b.write(Long(self.key_fingerprint))
        
        b.write(self.protocol.write())
        
        return b.getvalue()

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


class PhoneCall(Object):
    """Attributes:
        ID: ``0xffe6ab67``

    Args:
        id: ``int`` ``64-bit``
        access_hash: ``int`` ``64-bit``
        date: ``int`` ``32-bit``
        admin_id: ``int`` ``32-bit``
        participant_id: ``int`` ``32-bit``
        g_a_or_b: ``bytes``
        key_fingerprint: ``int`` ``64-bit``
        protocol: :obj:`PhoneCallProtocol <pyrogram.api.types.PhoneCallProtocol>`
        connection: :obj:`PhoneConnection <pyrogram.api.types.PhoneConnection>`
        alternative_connections: List of :obj:`PhoneConnection <pyrogram.api.types.PhoneConnection>`
        start_date: ``int`` ``32-bit``
    """

    ID = 0xffe6ab67

    def __init__(self, id: int, access_hash: int, date: int, admin_id: int, participant_id: int, g_a_or_b: bytes, key_fingerprint: int, protocol, connection, alternative_connections: list, start_date: int):
        self.id = id  # long
        self.access_hash = access_hash  # long
        self.date = date  # int
        self.admin_id = admin_id  # int
        self.participant_id = participant_id  # int
        self.g_a_or_b = g_a_or_b  # bytes
        self.key_fingerprint = key_fingerprint  # long
        self.protocol = protocol  # PhoneCallProtocol
        self.connection = connection  # PhoneConnection
        self.alternative_connections = alternative_connections  # Vector<PhoneConnection>
        self.start_date = start_date  # int

    @staticmethod
    def read(b: BytesIO, *args) -> "PhoneCall":
        # No flags
        
        id = Long.read(b)
        
        access_hash = Long.read(b)
        
        date = Int.read(b)
        
        admin_id = Int.read(b)
        
        participant_id = Int.read(b)
        
        g_a_or_b = Bytes.read(b)
        
        key_fingerprint = Long.read(b)
        
        protocol = Object.read(b)
        
        connection = Object.read(b)
        
        alternative_connections = Object.read(b)
        
        start_date = Int.read(b)
        
        return PhoneCall(id, access_hash, date, admin_id, participant_id, g_a_or_b, key_fingerprint, protocol, connection, alternative_connections, start_date)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        b.write(Long(self.access_hash))
        
        b.write(Int(self.date))
        
        b.write(Int(self.admin_id))
        
        b.write(Int(self.participant_id))
        
        b.write(Bytes(self.g_a_or_b))
        
        b.write(Long(self.key_fingerprint))
        
        b.write(self.protocol.write())
        
        b.write(self.connection.write())
        
        b.write(Vector(self.alternative_connections))
        
        b.write(Int(self.start_date))
        
        return b.getvalue()

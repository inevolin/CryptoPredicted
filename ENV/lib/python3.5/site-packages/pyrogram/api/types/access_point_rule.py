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


class AccessPointRule(Object):
    """Attributes:
        ID: ``0x4679b65f``

    Args:
        phone_prefix_rules: ``str``
        dc_id: ``int`` ``32-bit``
        ips: :obj:`vector<IpPort> <pyrogram.api.types.vector<IpPort>>`
    """

    ID = 0x4679b65f

    def __init__(self, phone_prefix_rules: str, dc_id: int, ips):
        self.phone_prefix_rules = phone_prefix_rules  # string
        self.dc_id = dc_id  # int
        self.ips = ips  # vector<IpPort>

    @staticmethod
    def read(b: BytesIO, *args) -> "AccessPointRule":
        # No flags
        
        phone_prefix_rules = String.read(b)
        
        dc_id = Int.read(b)
        
        ips = Object.read(b)
        
        return AccessPointRule(phone_prefix_rules, dc_id, ips)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.phone_prefix_rules))
        
        b.write(Int(self.dc_id))
        
        b.write(Vector(self.ips))
        
        return b.getvalue()

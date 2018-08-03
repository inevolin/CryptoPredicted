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


class Ping(Object):
    """Attributes:
        ID: ``0x7abe77ec``

    Args:
        ping_id: ``int`` ``64-bit``

    Raises:
        :obj:`Error <pyrogram.Error>`

    Returns:
        :obj:`Pong <pyrogram.api.types.Pong>`
    """

    ID = 0x7abe77ec

    def __init__(self, ping_id: int):
        self.ping_id = ping_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "Ping":
        # No flags
        
        ping_id = Long.read(b)
        
        return Ping(ping_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.ping_id))
        
        return b.getvalue()

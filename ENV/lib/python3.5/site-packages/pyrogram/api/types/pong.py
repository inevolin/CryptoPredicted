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


class Pong(Object):
    """Attributes:
        ID: ``0x347773c5``

    Args:
        msg_id: ``int`` ``64-bit``
        ping_id: ``int`` ``64-bit``

    See Also:
        This object can be returned by :obj:`Ping <pyrogram.api.functions.Ping>` and :obj:`PingDelayDisconnect <pyrogram.api.functions.PingDelayDisconnect>`.
    """

    ID = 0x347773c5

    def __init__(self, msg_id: int, ping_id: int):
        self.msg_id = msg_id  # long
        self.ping_id = ping_id  # long

    @staticmethod
    def read(b: BytesIO, *args) -> "Pong":
        # No flags
        
        msg_id = Long.read(b)
        
        ping_id = Long.read(b)
        
        return Pong(msg_id, ping_id)

    def write(self) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.msg_id))
        
        b.write(Long(self.ping_id))
        
        return b.getvalue()
